# LMS Skill

Future-reserved skill for Learning Management System integration.

## Planned Tools

- `submit_training_job_tool(dataset_path, model_name)` — Submit fine-tuning
- `get_eval_curriculum_tool()` — Get eval training modules

## Server

```bash
python3 skills/lms/server.py
# port: 8013
```

## Registration

Added to `scripts/core/config.py` as port 8013.
