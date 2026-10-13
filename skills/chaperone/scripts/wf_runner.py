#!/usr/bin/env python3
"""Run evops workflow.yaml steps sequentially with env substitution."""
import os, sys, yaml, re, subprocess

def expand_envs(obj, env):
    if isinstance(obj, str):
        for k, v in env.items():
            obj = obj.replace(f"${k}", str(v)).replace(f"${{{k}}}", str(v))
        return obj
    if isinstance(obj, list):
        return [expand_envs(x, env) for x in obj]
    if isinstance(obj, dict):
        return {k: expand_envs(v, env) for k, v in obj.items()}
    return obj

def run_step(step, env):
    action = step.get("action", "")
    action = expand_envs(action, env)
    print(f"\n[chaperone] step: {step['id']} — {step['name']}")
    # replace line continuations for subprocess
    cmd = action.replace("\\\n", " ")
    result = subprocess.run(cmd, shell=True, executable="/bin/bash")
    if result.returncode != 0:
        print(f"[chaperone] FAILED: {step['id']}")
        return False
    print(f"[chaperone] OK: {step['id']}")
    return True

def run(wf_path: str):
    with open(wf_path, "r", encoding="utf-8") as f:
        wf = yaml.safe_load(f)
    env = dict(os.environ)
    env.update(wf.get("env", {}))
    env.setdefault("WORKSPACE", "/tmp/evops_run")
    os.makedirs(env["WORKSPACE"], exist_ok=True)
    for step in wf.get("steps", []):
        if not run_step(step, env):
            print("[chaperone] workflow halted")
            return 1
    print("[chaperone] workflow complete")
    return 0

if __name__ == "__main__":
    sys.exit(run(sys.argv[1] if len(sys.argv) > 1 else "/home/bons/evops/workflow.yaml"))
