#!/usr/bin/env python3
"""Execute installed adapter commands, including cases met during real setup."""
import hashlib
import json
import pathlib
import subprocess
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parents[1]


class SetupSmokeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name) / 'codex'
        self.root.mkdir()
        self.install('codex')

    def install(self, runtime):
        if runtime == 'claude':
            # A host switch is a migration, not a second adapter on the same target.
            self.root = pathlib.Path(self.tmp.name) / 'claude'
            self.root.mkdir(exist_ok=True)
        result = self.run_command([sys.executable, str(REPO / 'install.py'),
                                   '--target', str(self.root), '--runtime', runtime, '--apply'])
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def run_command(self, argv, payload=None, cwd=None, shell=False):
        return subprocess.run(argv, cwd=str(cwd or self.root), shell=shell,
                              input=json.dumps(payload) if payload is not None else None,
                              capture_output=True, text=True, encoding='utf-8',
                              errors='replace', timeout=30)

    def hook(self, patch):
        result = self.run_command([sys.executable, str(self.root / 'harness/codex/hook.py')],
                                  {'hook_event_name': 'PreToolUse', 'tool_name': 'apply_patch',
                                   'tool_input': {'command': patch}})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return json.loads(result.stdout)

    def test_codex_move_destination_outside_project_is_denied(self):
        response = self.hook('*** Begin Patch\n*** Update File: docs/ARCHITECTURE.md\n'
                             '*** Move to: ../escape.md\n@@\n-old\n+new\n*** End Patch')
        self.assertEqual(response.get('hookSpecificOutput', {}).get('permissionDecision'), 'deny')

    def test_codex_add_outside_project_is_denied(self):
        response = self.hook('*** Begin Patch\n*** Add File: ../escape.md\n+data\n*** End Patch')
        self.assertEqual(response.get('hookSpecificOutput', {}).get('permissionDecision'), 'deny')

    def test_codex_valid_move_snapshots_source_and_existing_destination(self):
        source = self.root / 'docs/ARCHITECTURE.md'
        target = self.root / 'docs/moved.md'
        target.write_text('existing target', encoding='utf-8')
        response = self.hook('*** Begin Patch\n*** Update File: docs/ARCHITECTURE.md\n'
                             '*** Move to: docs/moved.md\n@@\n-old\n+new\n*** End Patch')
        self.assertNotEqual(response.get('hookSpecificOutput', {}).get('permissionDecision'), 'deny')
        manifests = list((self.root / 'harness/snapshots').glob('*/manifest.json'))
        self.assertEqual(len(manifests), 1)
        entries = json.loads(manifests[0].read_text(encoding='utf-8'))['files']
        self.assertEqual({x['path'] for x in entries}, {'docs/ARCHITECTURE.md', 'docs/moved.md'})
        for entry in entries:
            self.assertEqual(entry['sha256'], hashlib.sha256((self.root / entry['path']).read_bytes()).hexdigest())
        self.assertTrue(source.is_file())

    def test_theory_id_does_not_match_longer_identifier(self):
        (self.root / 'docs/CRITERIA.md').write_text('REQ-1234 exists; REQ-123-extra exists', encoding='utf-8')
        (self.root / 'harness/active-task.json').write_text(json.dumps({
            'status': 'ACTIVE', 'goal_id': 'G-1', 'theory_ids': ['REQ-123'],
            'tests': ['tests/example.py'], 'evidence': []}), encoding='utf-8')
        result = self.run_command([sys.executable, str(self.root / 'harness/common/task.py'), '--stage', 'plan'])
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)

    def test_codex_preflight_rejects_empty_handlers_and_invalid_timeout(self):
        path = self.root / '.codex/hooks.json'
        original = json.loads(path.read_text(encoding='utf-8'))
        for empty in (True, False):
            with self.subTest(empty_handlers=empty):
                data = json.loads(json.dumps(original))
                group = data['hooks']['PreToolUse'][0]
                if empty:
                    group['hooks'] = []
                else:
                    group['hooks'][0]['timeout'] = True
                path.write_text(json.dumps(data), encoding='utf-8')
                result = self.run_command([sys.executable, str(self.root / 'harness/codex/preflight.py')])
                self.assertEqual(result.returncode, 2, result.stdout + result.stderr)

    def test_claude_hook_command_works_from_nested_cwd(self):
        self.install('claude')
        settings = json.loads((self.root / '.claude/settings.json').read_text(encoding='utf-8'))
        command = settings['hooks']['UserPromptSubmit'][0]['hooks'][0]['command']
        result = self.run_command(command, {'hook_event_name': 'UserPromptSubmit'},
                                  cwd=self.root / 'docs/reports', shell=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('Bootstrap', result.stdout)

    def test_claude_protected_absolute_path_returns_native_context(self):
        self.install('claude')
        result = self.run_command([sys.executable, str(self.root / 'harness/claude/hook.py')], {
            'hook_event_name': 'PreToolUse', 'tool_name': 'Edit',
            'tool_input': {'file_path': str(self.root / 'docs/CRITERIA.md')}})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertTrue(result.stdout.strip().startswith('{'), result.stdout)
        context = json.loads(result.stdout)['hookSpecificOutput']
        self.assertEqual(context['hookEventName'], 'PreToolUse')
        self.assertIn('PROTECTED-SCOPE GUIDANCE', context['additionalContext'])
        self.assertIn('snapshot', context['additionalContext'])

    def test_claude_multiedit_top_level_file_is_snapshotted(self):
        self.install('claude')
        path = self.root / 'docs/ARCHITECTURE.md'
        result = self.run_command([sys.executable, str(self.root / 'harness/claude/hook.py')], {
            'hook_event_name': 'PreToolUse', 'tool_name': 'MultiEdit',
            'tool_input': {'file_path': str(path), 'edits': [
                {'old_string': 'a', 'new_string': 'b'}]}})
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('snapshot', result.stdout.lower())
        self.assertEqual(len(list((self.root / 'harness/snapshots').glob('*/manifest.json'))), 1)

    def test_claude_preflight_handles_non_object_policy(self):
        self.install('claude')
        (self.root / 'harness/hook-policy.json').write_text('[]', encoding='utf-8')
        result = self.run_command([sys.executable, str(self.root / 'harness/claude/preflight.py')])
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertNotIn('Traceback', result.stderr)

    def test_claude_stop_validates_checks_and_bounds_retry(self):
        self.install('claude')
        command = [sys.executable, str(self.root / 'harness/claude/hook.py')]
        idle = self.run_command(command, {'hook_event_name': 'Stop'})
        self.assertEqual(idle.returncode, 0)
        (self.root / 'docs/CRITERIA.md').write_text('REQ-123', encoding='utf-8')
        (self.root / 'docs/reports/proof.txt').write_text('test fixture', encoding='utf-8')
        (self.root / 'harness/active-task.json').write_text(json.dumps({
            'status': 'ACTIVE', 'goal_id': 'G-1', 'theory_ids': ['REQ-123'],
            'tests': ['docs/CRITERIA.md'], 'evidence': ['docs/reports/proof.txt']}), encoding='utf-8')
        checks = self.root / 'harness/common/checks.json'
        checks.write_text(json.dumps({'checks': [{'name': 'failure',
            'argv': [sys.executable, '-c', 'raise SystemExit(7)']}]}), encoding='utf-8')
        failed = self.run_command(command, {'hook_event_name': 'Stop'})
        self.assertEqual(failed.returncode, 2, failed.stdout + failed.stderr)
        bounded = self.run_command(command, {'hook_event_name': 'Stop', 'stop_hook_active': True})
        self.assertEqual(bounded.returncode, 0)
        self.assertIn('bounded retry', bounded.stderr)
        checks.write_text(json.dumps({'checks': [{'name': 'success',
            'argv': [sys.executable, '-c', 'raise SystemExit(0)']}]}), encoding='utf-8')
        passed = self.run_command(command, {'hook_event_name': 'Stop'})
        self.assertEqual(passed.returncode, 0, passed.stdout + passed.stderr)
        self.assertIn('script checks passed', passed.stdout)


if __name__ == '__main__':
    unittest.main(verbosity=2)
