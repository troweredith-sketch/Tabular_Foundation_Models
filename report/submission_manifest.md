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

## Historical / Non-Final Artifacts

The official result source of truth is the report package, the key CSV files listed above, and the generated figures in `results/figures/`.

The repository also keeps earlier trace artifacts such as `results/first_result.csv`, `results/phase3_*`, and `results/*backup.csv`. These files document the project path and review history, but they are not the final benchmark outputs used for the submitted conclusions.

Planning documents and notebooks, including `docs/phase_plan.md` and `notebooks/`, are retained as historical context. They should not override the final report, committed key CSV files, or this manifest.

## Experiment Scope Covered

- Mainline comparison of LightGBM, XGBoost, TabPFN v2, and TabICL on Adult and Bank Marketing.
- Phase 5 train-size scalability analysis over 512, 2048, 8192, 10000, and full train sizes.
- Phase 6 Big Plus negative ablation on TabICL support-set selection for Adult.
- Supplemental Adult missingness robustness sanity check at train size 2048 and seed 42.

The Phase 6 result should be presented as a negative ablation: budget-limited support sets reduce runtime, but the frozen Balanced Prototype Retrieval rule does not outperform Random Subset or Balanced Random Subset.

## Reproduction and Verification

Recommended setup:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-reproduce.txt
```

Lightweight checks:

```bash
python -m unittest discover -s tests
python3 src/render_reports.py
```

The final CSV and figures are committed. Re-running Phase 4, Phase 5, or Phase 6 final experiments is only needed when intentionally reproducing the frozen experiment artifacts from scratch.

## Timing and Hardware Context

- Submitted environment: WSL Ubuntu, Python 3.12.3.
- CPU: AMD Ryzen 7 8845H.
- GPU for foundation-model final runs: NVIDIA GeForce RTX 4060 Laptop GPU.
- Runtime columns are practical mixed-device timings, not same-device normalized speed benchmarks.
- Table 1 runtime comes from the Phase 4 mainline output; Table 2 and Figure 4 runtime come from the independent Phase 5 scalability output.
- TabICL checkpoint availability is prepared before the main loop; checkpoint download/setup is not intended to be counted in per-run timing.

## Explicitly Not Done / Caveats

- TALENT, TabArena, and other external benchmark suites were not run; Adult and Bank Marketing are a lightweight OpenML benchmark subset.
- LightGBM and XGBoost are fixed strong baselines, not tuned state-of-the-art baselines.
- Phase 7 was not started.
- The frozen Phase 6 method definition was not changed, but `src/phase6_big_plus_adult.py` now has a safer `--preset smoke|final` interface and records selection/end-to-end timing in the committed Phase 6 artifacts.
- The supplemental missingness check is a small Adult-only, single-seed sanity check, not a full robustness benchmark.
- `requirements-basic.txt` is the minimal install list, `requirements-reproduce.txt` pins the core reproduction/report-rendering environment, `requirements-lock.txt` records the key submitted package versions, and `requirements-freeze.txt` is the full transitive `.venv` snapshot.
- Detail CSV `data_cache` fields use repository-relative paths such as `data/raw/adult_openml.csv` rather than author-machine absolute paths.
