#!/usr/bin/env node
// Minimal chaperone CLI wrapper around wf_runner.py / wf_validator.py
const { execSync } = require('child_process');
const path = require('path');

const SKILL_DIR = path.dirname(path.dirname(__filename));
const WF_DEFAULT = '/home/bons/evops/workflow.yaml';

function usage() {
  console.log('Usage: chaperone-cli.js <run|validate|status> [workflow.yaml]');
  process.exit(1);
}

const cmd = process.argv[2];
const wf = process.argv[3] || WF_DEFAULT;

if (!cmd) usage();

try {
  if (cmd === 'validate') {
    execSync(`python ${SKILL_DIR}/scripts/wf_validator.py ${wf}`, { stdio: 'inherit' });
  } else if (cmd === 'run') {
    execSync(`python ${SKILL_DIR}/scripts/wf_runner.py ${wf}`, { stdio: 'inherit' });
  } else if (cmd === 'status') {
    console.log(`workflow: ${wf}`);
    console.log('state file not yet implemented');
  } else {
    usage();
  }
} catch (e) {
  process.exit(e.status || 1);
}
