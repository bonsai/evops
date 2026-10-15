---
description: "EVOPSの資料を1ページずつ検査し、内容JSON・SVG・既存CSSの整合性とVLM-MCP判定を記録する"
intent: "ページ単位の品質ゲートを運用し、実検査されていないページを合格扱いせず、PASS後にだけ次ページへ進める"
on:
  workflow_dispatch:
    inputs:
      page_id:
        description: "検査するページID（初回は p26-kaguru-agent-kaggle-evops-workflow）"
        required: true
        type: string
        default: "p26-kaguru-agent-kaggle-evops-workflow"
permissions:
  contents: read
concurrency:
  job-discriminator: ${{ github.run_id }}
---

# EVOPS Page Quality Gate

## Mission

ページを一度に一つだけ検査する。初回対象は次のページに限定する。

- Page ID: `p26-kaguru-agent-kaggle-evops-workflow`
- Content contract: `docs/40-submit/page-tests/p26-kaguru-agent-kaggle-evops-workflow/content.json`
- Test record: `docs/40-submit/page-tests/p26-kaguru-agent-kaggle-evops-workflow/test.json`
- HTML: `docs/40-submit/part02_deliver.html`
- SVG: `docs/40-submit/figures/evops-system-overview.svg`

Do not expand to another page during this run.

## Procedure

1. Read the page's content JSON, test JSON, HTML section, referenced SVG, and any CSS actually loaded by that HTML. Treat the repository's existing HTML/CSS pattern as canonical; do not create page-specific CSS.
2. Check that the JSON's title, purpose, stages, diagram path, alt text, and caption agree with the HTML and SVG. Check referenced files and paths.
3. Run available deterministic checks for JSON parsing, SVG/XML validity, required SVG `viewBox`, and references. If the environment supports browser rendering, render this page and inspect the screenshot; do not claim a render occurred unless an actual screenshot was produced.
4. Use the configured VLM-MCP to judge the rendered screenshot for legibility, clipping, overlaps, spacing, contrast, and consistency between the figure and the page text. Return structured findings with severity and evidence.
5. If VLM-MCP or screenshot capture is unavailable, mark that gate BLOCKED/NOT_RUN. Never simulate or infer a VLM-MCP result from source code.
6. Report only concrete mismatches and smallest necessary fixes. Do not modify other pages. Do not mark PASS if any required gate is blocked or a critical issue remains.

## Decision policy

- `PASS`: content, structure, loaded CSS/template, actual rendering, and VLM-MCP visual review all pass.
- `FAIL`: a verified mismatch or visual defect requires correction.
- `HOLD`: a required tool or evidence is unavailable.
- A page marked PASS is eligible for the next page; otherwise keep work on the same page.

## Output format

Return one JSON object in the run report:

```json
{
  "page_id": "p26-kaguru-agent-kaggle-evops-workflow",
  "decision": "PASS | FAIL | HOLD",
  "gates": {
    "content_json": "PASS | FAIL",
    "html_svg_consistency": "PASS | FAIL",
    "existing_css": "PASS | FAIL | NOT_APPLICABLE",
    "deterministic_checks": "PASS | FAIL | NOT_RUN",
    "browser_render": "PASS | FAIL | NOT_RUN",
    "vlm_mcp": "PASS | FAIL | BLOCKED"
  },
  "findings": [
    {
      "severity": "critical | major | minor",
      "file": "repository-relative path",
      "evidence": "specific observed evidence",
      "fix": "smallest necessary correction"
    }
  ],
  "next_action": "one concrete action"
}
```

## Guardrails

- Do not invent test results, screenshots, MCP responses, scores, or citations.
- Do not rewrite content merely for stylistic preference.
- Keep JSON, SVG, and existing HTML/CSS template aligned.
- One run equals one page. Re-test the same page after fixes before moving on.
