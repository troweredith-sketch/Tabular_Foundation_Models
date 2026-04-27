# Submission Manifest

This file summarizes the final report package and the supporting artifacts for handoff/submission.

## Final Deliverables

- Official English report PDF: `report/final_report.pdf`
- Chinese study/reference PDF: `report/final_report_zh_study.pdf`

The English PDF is the formal submission version. The Chinese PDF is a study aid for review, explanation, and presentation preparation.

## Source Reports

- English source Markdown: `report/report_draft.md`
- Chinese study source Markdown: `report/report_draft_zh.md`
- English draft PDF used to create the final copy: `report/report_draft.pdf`
- Chinese draft PDF used to create the final copy: `report/report_draft_zh.pdf`

## Figures

Main figure directory: `results/figures/`

Key report figures:

- `results/figures/phase5_scalability_accuracy.png`
- `results/figures/phase5_scalability_balanced_accuracy.png`
- `results/figures/phase5_scalability_macro_f1.png`
- `results/figures/phase5_scalability_total_seconds_median.png`
- `results/figures/phase6_big_plus_adult_bpr_delta.png`

Supporting Phase 6 figures are also available in the same directory:

- `results/figures/phase6_big_plus_adult_accuracy.png`
- `results/figures/phase6_big_plus_adult_balanced_accuracy.png`
- `results/figures/phase6_big_plus_adult_macro_f1.png`
- `results/figures/phase6_big_plus_adult_total_seconds_median.png`

PDF versions of the generated figures are also present in `results/figures/`.

## Key Result CSV Files

- Mainline raw comparison results: `results/phase4_mainline_compare.csv`
- Mainline summary results: `results/phase4_mainline_compare_summary.csv`
- Phase 5 scalability raw results: `results/phase5_scalability_compare.csv`
- Phase 5 scalability summary results: `results/phase5_scalability_compare_summary.csv`
- Phase 6 Big Plus Adult raw results: `results/phase6_big_plus_adult.csv`
- Phase 6 Big Plus Adult summary results: `results/phase6_big_plus_adult_summary.csv`
- Supplemental Adult missingness robustness raw results: `results/missingness_robustness_adult.csv`
- Supplemental Adult missingness robustness summary results: `results/missingness_robustness_adult_summary.csv`

## Experiment Scope Covered

- Mainline comparison of LightGBM, XGBoost, TabPFN v2, and TabICL on Adult and Bank Marketing.
- Phase 5 train-size scalability analysis over 512, 2048, 8192, 10000, and full train sizes.
- Phase 6 Big Plus negative ablation on TabICL support-set selection for Adult.
- Supplemental Adult missingness robustness sanity check at train size 2048 and seed 42.

The Phase 6 result should be presented as a negative ablation: budget-limited support sets reduce runtime, but the frozen Balanced Prototype Retrieval rule does not outperform Random Subset or Balanced Random Subset.

## Explicitly Not Done / Caveats

- Phase 7 was not started.
- The frozen Phase 6 method definition was not changed, but `src/phase6_big_plus_adult.py` now has a safer `--preset smoke|final` interface and records selection/end-to-end timing in the committed Phase 6 artifacts.
- The supplemental missingness check is a small sanity check, not a full robustness benchmark.
- `requirements-basic.txt` is the minimal install list, `requirements-lock.txt` records the key submitted package versions, and `requirements-freeze.txt` is the full transitive `.venv` snapshot.
