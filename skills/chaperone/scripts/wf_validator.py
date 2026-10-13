#!/usr/bin/env python3
"""Validate evops workflow.yaml schema."""
import sys, yaml

REQUIRED_TOP = {"name", "description", "env", "steps"}
REQUIRED_STEP = {"id", "name", "action"}

def validate(path: str):
    with open(path, "r", encoding="utf-8") as f:
        wf = yaml.safe_load(f)
    missing = REQUIRED_TOP - set(wf.keys())
    if missing:
        print(f"FAIL: missing top keys: {missing}")
        return 1
    seen_ids = set()
    for i, step in enumerate(wf.get("steps", [])):
        miss = REQUIRED_STEP - set(step.keys())
        if miss:
            print(f"FAIL step {i}: missing {miss}")
            return 1
        if step["id"] in seen_ids:
            print(f"FAIL duplicate id: {step['id']}")
            return 1
        seen_ids.add(step["id"])
    print("OK: workflow.yaml is valid")
    return 0

if __name__ == "__main__":
    sys.exit(validate(sys.argv[1] if len(sys.argv) > 1 else "/home/bons/evops/workflow.yaml"))
