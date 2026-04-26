# Tabular Foundation Models

Course project repository for comparing tabular foundation models with boosted-tree baselines on small-to-medium tabular classification tasks.

## Current Status

The project is submission-ready.

Final deliverables:

- Official English report: `report/final_report.pdf`
- Chinese study/reference report: `report/final_report_zh_study.pdf`
- Submission manifest: `report/submission_manifest.md`

The official submission file is `report/final_report.pdf`. The Chinese PDF is for learning, review, and presentation preparation.

## Project Question

> We compare tabular foundation models with boosted-tree baselines on small-to-medium tabular classification datasets, and we further explore whether support-set selection can improve TabICL.

The project focuses on classification only. Regression and survival analysis are out of scope.

## Models

Mainline models:

- LightGBM
- XGBoost
- TabPFN v2
- TabICL

Big Plus extension:

- TabICL support-set selection on Adult

## Datasets

Main datasets:

- Adult
- Bank Marketing

Early exploration also considered Credit-G, but the final report focuses on Adult and Bank Marketing.

## Experiment Scope

The final report covers:

- Mainline comparison of LightGBM, XGBoost, TabPFN v2, and TabICL.
- Phase 5 train-size scalability analysis over `512`, `2048`, `8192`, `10000`, and `full`.
- Phase 6 Big Plus negative ablation on TabICL support-set selection for Adult.

Phase 7 was not started.

## Key Results

Mainline findings:

- On Adult, boosted-tree baselines remain strongest overall.
- On Bank Marketing, foundation models are more competitive, especially TabICL on imbalance-aware metrics.
- Tree models are much faster than the foundation models.
- TabICL is substantially faster than TabPFN v2 in this local setup.

Phase 6 Big Plus finding:

- Budget-limited support sets substantially reduce TabICL runtime.
- The frozen Balanced Prototype Retrieval strategy does not outperform Random Subset or Balanced Random Subset.
- The Phase 6 result should be treated as a useful negative ablation, not as a successful new method.

## Repository Layout

- `report/`: final reports, source Markdown, and submission manifest.
- `results/`: CSV results and generated figures.
- `results/figures/`: PNG/PDF figures used by the report.
- `src/`: experiment and figure-generation scripts.
- `notebooks/`: learning notes and phase summaries.
- `docs/`: project logs, phase plans, and handoff notes.
- `slides/`: presentation outline drafts.
- `data/`: local data directory.

## Final Report Files

- `report/final_report.pdf`: official English report for submission.
- `report/report_draft.md`: English source Markdown.
- `report/final_report_zh_study.pdf`: Chinese study/reference report.
- `report/report_draft_zh.md`: Chinese source Markdown.
- `report/submission_manifest.md`: handoff checklist with report, figure, and CSV paths.

## Key Result Files

- `results/phase4_mainline_compare.csv`
- `results/phase4_mainline_compare_summary.csv`
- `results/phase5_scalability_compare.csv`
- `results/phase5_scalability_compare_summary.csv`
- `results/phase6_big_plus_adult.csv`
- `results/phase6_big_plus_adult_summary.csv`

## Main Figures

- `results/figures/phase5_scalability_accuracy.png`
- `results/figures/phase5_scalability_balanced_accuracy.png`
- `results/figures/phase5_scalability_macro_f1.png`
- `results/figures/phase5_scalability_total_seconds_median.png`
- `results/figures/phase6_big_plus_adult_bpr_delta.png`

Supporting Phase 6 figures are also available in `results/figures/`.

## Environment

Recommended environment: WSL Ubuntu with a project-local virtual environment.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-basic.txt
```

Some foundation-model runs may require additional packages and CUDA support, depending on the local machine.

## Reproducing Main Artifacts

The final CSV and figures are already committed. To rerun experiments from scratch, use the scripts below only when intentionally reproducing results.

Mainline comparison:

```bash
source .venv/bin/activate
python3 src/phase4_mainline_compare.py
```

Phase 5 scalability comparison:

```bash
python3 src/phase5_scalability_compare.py
python3 src/phase5_make_mainline_figures.py
```

Phase 6 Big Plus Adult experiment:

```bash
python3 src/phase6_big_plus_adult.py
python3 src/phase6_make_big_plus_figures.py
```

These commands can be expensive. They are not needed just to inspect the final report.

## Documentation Handoff

For project context, read:

1. `report/submission_manifest.md`
2. `docs/session_handoff.md`
3. `docs/project_record.md`
4. `docs/phase_plan.md`
5. `docs/big_plus_plan.md`
6. `notebooks/phase6_big_plus_adult.md`

The handoff notes explicitly record that Phase 7 was not started, final packaging did not rerun experiments, and the Phase 6 frozen method definition was not modified during report finalization.
