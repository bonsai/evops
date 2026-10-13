# Chaperone — evops Workflow Manager

`chaperone` reads `evops/workflow.yaml` and runs each step as a loosely-coupled CLI/MCP call.

## Quick start

```bash
# validate
python skills/chaperone/scripts/wf_validator.py workflow.yaml

# run the whole pipeline
python skills/chaperone/scripts/wf_runner.py workflow.yaml

# or via node CLI
node skills/chaperone/cli/chaperone-cli.js run workflow.yaml
```

## Design rules

- Only `workflow.yaml` and JSON artifacts are shared between steps.
- `chaperone` never imports internal code of `telop`, `videogen`, `kamishibai`, etc.
- Each step returns `{status, output_file}`; failures pause the workflow.

## Commands

| Command | Description |
|--------|-------------|
| `run <wf>` | Execute all steps |
| `status` | Show latest run state |
| `step <id>` | Run a single step |

## Default ports it knows

- videogen: 8006
- sf-paper-comic: 8004
- evaluator: 8002
- bpy-gen: 8005
- voicevox: 50021
