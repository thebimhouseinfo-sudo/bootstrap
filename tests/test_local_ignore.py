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
                               str(self.root), *args], capture_output=True, text=True,
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
        for runtime in ('codex', 'claude', 'continue'):
            with self.subTest(runtime=runtime):
                installed = self.install('--runtime', runtime, '--apply')
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
            self.assertFalse(path.startswith(('.codex/', '.claude/', '.agents/', '.continue/',
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


if __name__ == '__main__':
    unittest.main(verbosity=2)
