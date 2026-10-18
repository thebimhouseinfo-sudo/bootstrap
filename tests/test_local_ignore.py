#!/usr/bin/env python3
"""Privacy of installed agent setup, tested with a real disposable Git index."""
import pathlib
import subprocess
import sys
import tempfile
import unittest

REPO = pathlib.Path(__file__).resolve().parents[1]


class LocalIgnoreTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = pathlib.Path(self.tmp.name)
        self.git('init', '-q')

    def git(self, *args):
        result = subprocess.run(['git', '-C', str(self.root), *args], capture_output=True,
                                text=True, encoding='utf-8', errors='replace', timeout=20)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return result.stdout

    def install(self, *args):
        return subprocess.run([sys.executable, str(REPO / 'install.py'), '--target',
                               str(self.root), *([] if '--runtime' in args else ['--runtime', 'codex']), *args], capture_output=True, text=True,
                              encoding='utf-8', errors='replace', timeout=30)

    def test_existing_ignore_preserved_preview_and_apply_are_idempotent(self):
        path = self.root / '.gitignore'
        original = b'# product rules\r\n/build/\r\n!important.txt'
        path.write_bytes(original)
        preview = self.install()
        self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
        self.assertIn('UPDATE .gitignore', preview.stdout)
        self.assertEqual(path.read_bytes(), original)
        applied = self.install('--apply')
        self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
        first = path.read_bytes()
        self.assertTrue(first.startswith(original))
        again = self.install('--apply')
        self.assertEqual(again.returncode, 0, again.stdout + again.stderr)
        self.assertEqual(first, path.read_bytes())
        self.assertIn('SAME .gitignore', again.stdout)

    def test_git_add_keeps_only_source_and_product_docs_for_all_runtimes(self):
        for runtime in ('codex', 'antigravity', 'claude', 'continue', 'generic'):
            with self.subTest(runtime=runtime):
                installed = self.install('--runtime', runtime, *(['--target-app', 'cline'] if runtime == 'generic' else []), '--apply')
                self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
        (self.root / 'src').mkdir()
        (self.root / 'src/app.py').write_text('print(1)', encoding='utf-8')
        (self.root / 'docs/product.md').write_text('product documentation', encoding='utf-8')
        (self.root / 'README.md').write_text('product readme', encoding='utf-8')
        (self.root / 'harness/runtime.log').write_text('local log', encoding='utf-8')
        self.git('add', '.')
        tracked = set(self.git('ls-files').splitlines())
        self.assertTrue({'src/app.py', 'docs/product.md', 'README.md', '.gitignore'} <= tracked)
        self.assertTrue({'docs/CRITERIA.md', 'docs/ARCHITECTURE.md'} <= tracked)
        for path in tracked:
            self.assertFalse(path.startswith(('.codex/', '.antigravity/', '.claude/', '.agents/', '.continue/', '.generic/',
                                              'harness/', 'lessons/')), path)
        for path in ('AGENTS.md', 'CLAUDE.md', 'TASKS.md', 'docs/PROJECT_PROFILE.md',
                     'docs/TRACE.md', 'docs/reports/_TEMPLATE.md', 'docs/reports/_REVIEW_TEMPLATE.md'):
            self.assertNotIn(path, tracked)
        # Only installed target setup is ignored; bootstrap's distributable source stays versioned.
        result = subprocess.run(['git', '-C', str(REPO), 'ls-files',
                                 'project-template/harness/codex/hook.py'], capture_output=True,
                                text=True, timeout=10)
        self.assertIn('project-template/harness/codex/hook.py', result.stdout)
        future = subprocess.run(['git', '-C', str(REPO), 'check-ignore', '--no-index',
                                 'project-template/harness/codex/future_module.py'],
                                capture_output=True, text=True, timeout=10)
        self.assertEqual(future.returncode, 1, future.stdout + future.stderr)

    def test_tracked_local_setup_is_reported_without_deleting_or_untracking(self):
        path = self.root / '.codex/config.toml'
        path.parent.mkdir()
        original = (REPO / 'project-template/.codex/config.toml').read_bytes()
        path.write_bytes(original)
        self.git('add', '.codex/config.toml')
        result = self.install('--apply')
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn('TRACKED_LOCAL_SETUP: .codex/config.toml', result.stdout)
        self.assertEqual(path.read_bytes(), original)
        self.assertIn('.codex/config.toml', self.git('ls-files'))

    def test_managed_block_stays_last_and_existing_product_exceptions_survive(self):
        first = self.install('--apply')
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        path = self.root / '.gitignore'
        with path.open('ab') as output:
            output.write(b'\n# user product exceptions\n!/docs/product.md\n!/.codex/config.toml\n')
        result = self.install('--apply')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        content = path.read_text(encoding='utf-8')
        self.assertEqual(content.count('# BEGIN bootstrap local agent setup'), 1)
        self.assertIn('!/docs/product.md', content)
        self.assertTrue(content.endswith('# END bootstrap local agent setup\n'))
        ignored = self.git('check-ignore', '.codex/config.toml')
        self.assertIn('.codex/config.toml', ignored)
        snapshot = path.read_bytes()
        self.assertEqual(self.install('--apply').returncode, 0)
        self.assertEqual(snapshot, path.read_bytes())

    def test_malformed_managed_block_blocks_before_installing_any_files(self):
        path = self.root / '.gitignore'
        original = b'# BEGIN bootstrap local agent setup\n/user-pattern/\n'
        path.write_bytes(original)
        result = self.install('--apply')
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertEqual(path.read_bytes(), original)
        self.assertFalse((self.root / 'AGENTS.md').exists())
        self.assertFalse((self.root / '.codex').exists())

    def test_corrupt_repository_is_not_mistaken_for_non_git_project(self):
        (self.root / '.git/HEAD').write_text('invalid HEAD', encoding='utf-8')
        result = self.install('--apply')
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertFalse((self.root / 'AGENTS.md').exists())
        self.assertFalse((self.root / '.gitignore').exists())

    def test_nested_ignore_exception_blocks_before_copying_local_setup(self):
        docs = self.root / 'docs'
        docs.mkdir()
        child_ignore = docs / '.gitignore'
        child_ignore.write_text('!TRACE.md\n!PROJECT_PROFILE.md\n', encoding='utf-8')
        result = self.install('--apply')
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn('LOCAL_SETUP_NOT_IGNORED: docs/TRACE.md', result.stdout)
        self.assertFalse((self.root / 'AGENTS.md').exists())
        self.assertFalse((docs / 'TRACE.md').exists())
        self.assertEqual(child_ignore.read_text(encoding='utf-8'), '!TRACE.md\n!PROJECT_PROFILE.md\n')


    def test_local_mode_is_default_and_never_stages_agent_configuration(self):
        installed = self.install('--apply')
        self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
        self.assertIn('# mode: local', (self.root / '.gitignore').read_text(encoding='utf-8'))
        self.git('add', '-A')
        staged = set(self.git('ls-files').splitlines())
        self.assertNotIn('AGENTS.md', staged)
        self.assertNotIn('.codex/config.toml', staged)
        self.assertNotIn('harness/common/verify.py', staged)

    def test_tracked_mode_stages_config_but_never_local_state(self):
        installed = self.install('--config-git', 'tracked', '--apply')
        self.assertEqual(installed.returncode, 0, installed.stdout + installed.stderr)
        self.assertIn('Config in Git    : tracked', installed.stdout)
        self.assertIn('ALWAYS_LOCAL', installed.stdout)
        self.assertIn('# mode: tracked', (self.root / '.gitignore').read_text(encoding='utf-8'))
        (self.root / 'harness/approvals.jsonl').write_text('private approval', encoding='utf-8')
        (self.root / 'harness/chat-journal.jsonl').write_text('private journal', encoding='utf-8')
        (self.root / '.claude').mkdir(exist_ok=True)
        (self.root / '.claude/settings.local.json').write_text('{}', encoding='utf-8')
        self.git('add', '-A')
        staged = set(self.git('ls-files').splitlines())
        self.assertIn('AGENTS.md', staged)
        self.assertTrue(any(name.startswith('.agents/') for name in staged))
        self.assertIn('harness/common/verify.py', staged)
        for private in ('harness/approvals.jsonl', 'harness/chat-journal.jsonl',
                        'docs/TRACE.md', '.claude/settings.local.json'):
            self.assertNotIn(private, staged)
        self.assertNotIn('/harness/', (self.root / '.gitignore').read_text(encoding='utf-8').splitlines())

    def test_tracked_mode_nested_ignore_exception_blocks_before_copy(self):
        harness = self.root / 'harness'
        harness.mkdir()
        (harness / '.gitignore').write_text('!*.jsonl\n', encoding='utf-8')
        result = self.install('--config-git', 'tracked', '--apply')
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn('LOCAL_STATE_NOT_IGNORED: harness/approvals.jsonl', result.stdout)
        self.assertIn('ROLLBACK_RESTORED: .gitignore', result.stdout)
        self.assertFalse((self.root / 'AGENTS.md').exists())
        self.assertFalse((self.root / '.agents').exists())
        self.assertFalse((self.root / '.gitignore').exists())

    def test_tracked_mode_rejects_pretracked_local_state_without_index_changes(self):
        state = self.root / 'harness/approvals.jsonl'
        state.parent.mkdir()
        state.write_text('private approval', encoding='utf-8')
        self.git('add', 'harness/approvals.jsonl')
        before = self.git('ls-files')
        result = self.install('--config-git', 'tracked', '--apply')
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn('TRACKED_LOCAL_STATE: harness/approvals.jsonl', result.stdout)
        self.assertEqual(self.git('ls-files'), before)
        self.assertEqual(state.read_text(encoding='utf-8'), 'private approval')

    def test_tracked_mode_second_apply_is_idempotent(self):
        first = self.install('--config-git', 'tracked', '--apply')
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        path = self.root / '.gitignore'
        snapshot = path.read_bytes()
        again = self.install('--config-git', 'tracked', '--apply')
        self.assertEqual(again.returncode, 0, again.stdout + again.stderr)
        self.assertIn('SAME .gitignore', again.stdout)
        self.assertEqual(path.read_bytes(), snapshot)

    def test_mode_switch_requires_explicit_change_flag(self):
        self.assertEqual(self.install('--apply').returncode, 0)
        previous = (self.root / '.gitignore').read_bytes()
        for args in (('--config-git', 'tracked'),
                     ('--config-git', 'tracked', '--apply')):
            result = self.install(*args)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            self.assertIn('MODE_CHANGE_REQUIRES_APPROVAL: local -> tracked', result.stdout)
            self.assertEqual((self.root / '.gitignore').read_bytes(), previous)
        preview = self.install('--config-git', 'tracked', '--change-config-git')
        self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
        self.assertIn('UPDATE .gitignore', preview.stdout)
        self.assertEqual((self.root / '.gitignore').read_bytes(), previous)
        apply = self.install('--config-git', 'tracked', '--change-config-git', '--apply')
        self.assertEqual(apply.returncode, 0, apply.stdout + apply.stderr)
        self.assertIn('# mode: tracked', (self.root / '.gitignore').read_text(encoding='utf-8'))
        reverse = self.install('--apply')
        self.assertEqual(reverse.returncode, 2, reverse.stdout + reverse.stderr)
        self.assertIn('MODE_CHANGE_REQUIRES_APPROVAL: tracked -> local', reverse.stdout)

    def test_tracked_to_local_reports_pretracked_configuration(self):
        self.assertEqual(self.install('--config-git', 'tracked', '--apply').returncode, 0)
        self.git('add', 'AGENTS.md', '.agents', 'harness/common')
        staged_before = self.git('ls-files')
        result = self.install('--config-git', 'local', '--change-config-git', '--apply')
        self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
        self.assertIn('TRACKED_LOCAL_SETUP: AGENTS.md', result.stdout)
        self.assertEqual(self.git('ls-files'), staged_before)

    def test_legacy_block_without_mode_is_treated_as_local(self):
        first = self.install('--apply')
        self.assertEqual(first.returncode, 0, first.stdout + first.stderr)
        ignore = self.root / '.gitignore'
        legacy = ignore.read_bytes().replace(b'# mode: local\r\n', b'').replace(b'# mode: local\n', b'')
        ignore.write_bytes(legacy)
        preview = self.install()
        self.assertEqual(preview.returncode, 0, preview.stdout + preview.stderr)
        self.assertIn('UPDATE .gitignore', preview.stdout)
        self.assertNotIn('MODE_CHANGE_REQUIRES_APPROVAL', preview.stdout)
        applied = self.install('--apply')
        self.assertEqual(applied.returncode, 0, applied.stdout + applied.stderr)
        self.assertIn('# mode: local', ignore.read_text(encoding='utf-8'))
        self.assertIn('SAME .gitignore', self.install().stdout)

    def test_yes_flag_is_ignored_and_does_not_apply(self):
        result = self.install('--yes')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('IGNORED_FLAG', result.stdout)
        self.assertFalse((self.root / '.gitignore').exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
