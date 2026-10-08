# Paper Research Skill

## Purpose
Turn one paper PDF or URL into a reproducible research package:
- Markdown summary
- Mermaid concept map (.mmd)
- self-contained HTML reading page
- citation/source metadata

## Workflow
1. Resolve canonical title, authors, year, venue, DOI/arXiv.
2. Extract research question, method, data, evaluation, result, limitation.
3. Classify relevance against the current Intent.
4. Produce ID.md, ID.mmd, and ID.html.
5. Link all three from papers/index.html.
6. Update papers.jsonl with source, category, relevance, and status.
7. Record the exact claim supported; never infer evidence from an abstract alone.

## Selection policy
Prioritize papers that reduce uncertainty in:
1. VLM/LMM evaluation reliability
2. generation-method search / evolutionary selection
3. prompt/code optimization
4. quality-diversity and multiobjective search
5. uncertainty, confidence, human preference, and active learning
6. program synthesis when code is a generation genome

Prefer primary papers, recent benchmarks, and reproducible evaluation.

## Output schema
Markdown: Intent relevance, research question, method, experimental setup, findings, importable ideas, assumptions that cannot be made, limitations, source.
Mermaid: force the paper's causal/method concept into a simple graph.
HTML: readable without a build system.

## Principle
Do not collect papers for quantity. Select the smallest evidence set that changes the experiment design.
