#!/usr/bin/env node
'use strict';
// Continue CLI native Stop hook: only an ACTIVE and configured task is verified.
// Actual host dispatch is NOT established by this script-only fixture.
const fs = require('node:fs');
const path = require('node:path');
const cp = require('node:child_process');
const root = path.resolve(__dirname, '..', '..');
function read(rel) {
  try { return JSON.parse(fs.readFileSync(path.join(root, rel), 'utf8')); }
  catch { return {}; }
}
function emit(value) { process.stdout.write(JSON.stringify(value) + '\n'); }
function main() {
  const input = JSON.parse(fs.readFileSync(0,'utf8'));
  if (!input || input.hook_event_name !== 'Stop') return emit({});
  const setup = read('harness/setup-state.json');
  if (setup.phase === 'BOOTSTRAPPING') return emit({});
  const task = read('harness/active-task.json');
  const policy = read('harness/hook-policy.json');
  if (input.stop_hook_active || task.status !== 'ACTIVE' || policy.stop_verify !== true)
    return emit({});
  const python = process.env.PYTHON || (process.platform === 'win32' ? 'python' : 'python3');
  const work = cp.spawnSync(python, [path.join(root, 'harness/common/task.py'), 'validate'],
     {cwd:root, encoding:'utf8', timeout:120000});
  // Continue versions may not support blocking a Stop; return accurate evidence.
  if (work.error || work.status !== 0) {
    const why = (work.stderr || work.stdout || String(work.error || 'task validation failed')).slice(-1200);
    return emit({decision:'block',reason:'BOOTSTRAP_STOP_CHECK: '+why});
  }
  const verify = cp.spawnSync(python, [path.join(root,'harness/common/verify.py')],
    {cwd:root, encoding:'utf8', timeout:120000});
  if (verify.error || verify.status !== 0) {
    const why = (verify.stderr || verify.stdout || String(verify.error || 'verification failed')).slice(-1200);
    return emit({decision:'block', reason:'BOOTSTRAP_STOP_CHECK: '+why});
  }
  emit({});
}
try { main(); }
catch(err) { process.stderr.write('BOOTSTRAP_STOP_HOOK_ERROR: '+err.message+'\n'); process.exitCode=2; }
