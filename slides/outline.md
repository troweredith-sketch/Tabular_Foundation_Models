# 15-Minute Presentation Outline

## Slide 1: Project Title

- Key message: This project compares tabular foundation models with strong tree baselines on practical classification tasks.
- Suggested figure/table: None, or a simple title slide with the four model names and two dataset names.
- Speaker note bullets:
  - Introduce the project topic: tabular foundation models.
  - State the main models: TabPFN v2, TabICL, LightGBM, XGBoost.
  - State the main datasets: Adult and Bank Marketing.
  - Emphasize that the mainline is classification only.

## Slide 2: Motivation

- Key message: Tabular foundation models are promising, but boosted trees are still very strong and fast.
- Suggested figure/table: A small comparison matrix: foundation models vs tree baselines.
- Speaker note bullets:
  - Tabular data is common in applied ML.
  - Boosted trees are trusted baselines.
  - Foundation models may reduce task-specific modeling work.
  - The question is not only "who wins", but "when and at what cost".

## Slide 3: Research Questions

- Key message: The project studies predictive quality, scalability, and practical runtime.
- Suggested figure/table: Bullet summary of the three evaluation axes.
- Speaker note bullets:
  - Compare four models on two datasets.
  - Use accuracy, balanced accuracy, and macro-F1.
  - Study train-size scalability from 512 to full.
  - Track runtime as a practical usability signal.

## Slide 4: Datasets and Models

- Key message: The mainline uses two OpenML classification datasets and four fixed models.
- Suggested figure/table: Dataset/model setup table.
- Speaker note bullets:
  - Adult mixes numerical and categorical features.
  - Bank Marketing is more class-imbalanced.
  - LightGBM and XGBoost are fixed strong baselines.
  - TabPFN v2 and TabICL are the foundation-model baselines.

## Slide 5: Experimental Setup

- Key message: The comparison uses repeated stratified splits and fixed mainline settings.
- Suggested figure/table: Experimental protocol diagram.
- Speaker note bullets:
  - Seeds are 42, 43, 44, 45, and 46.
  - Within each seed, all models share the same split.
  - Across seeds, this is repeated stratified splitting, not one fixed test set.
  - Train-size grid: 512, 2048, 8192, 10000, full.
  - No new models, no tuning, no regression or survival tasks.

## Slide 6: Main Results on Adult

- Key message: Adult favors tree baselines, while TabICL is close but not clearly better.
- Suggested figure/table: Compact Adult rows from `results/phase4_mainline_compare_summary.csv`.
- Speaker note bullets:
  - XGBoost has the highest `control_10k` accuracy.
  - LightGBM has the strongest Adult balanced accuracy and macro-F1 in `control_10k`.
  - TabICL is close to the tree baselines.
  - TabPFN v2 is weaker on metrics and slower in runtime.

## Slide 7: Main Results on Bank Marketing

- Key message: Foundation models are stronger on Bank Marketing, especially TabICL on imbalance-aware metrics.
- Suggested figure/table: Compact Bank Marketing rows from `results/phase4_mainline_compare_summary.csv`.
- Speaker note bullets:
  - TabICL and TabPFN v2 tie on `control_10k` accuracy.
  - TabICL leads TabPFN v2 in balanced accuracy and macro-F1.
  - In full-train reference results, TabICL leads across the main metrics.
  - This dataset shows why accuracy alone is not enough.

## Slide 8: Train-Size Scalability

- Key message: More training data generally improves metrics, with different gains by dataset and model.
- Suggested figure/table: `results/figures/phase5_scalability_macro_f1.png`.
- Speaker note bullets:
  - Adult: tree models gain strongly from larger train sizes.
  - Bank Marketing: all models improve clearly on macro-F1.
  - TabICL reaches the strongest full-train macro-F1 on Bank Marketing.
  - TabPFN v2 improves less on Adult despite higher runtime cost.

## Slide 9: Runtime Scalability

- Key message: Runtime grows sharply for foundation models; TabICL is much faster than TabPFN v2.
- Suggested figure/table: `results/figures/phase5_scalability_total_seconds_median.png`.
- Speaker note bullets:
  - Runtime uses practical mixed-device timing.
  - Tree models run on CPU and remain fastest.
  - Foundation models may use CUDA, so this is not strict same-device benchmarking.
  - TabICL is consistently much faster than TabPFN v2 at larger train sizes.

## Slide 10: Model Tradeoffs

- Key message: The best model depends on dataset, metric, and runtime budget.
- Suggested figure/table: Pros/cons table for the four models.
- Speaker note bullets:
  - LightGBM: fast and strong, especially on Adult.
  - XGBoost: fast and competitive, with strong Adult accuracy.
  - TabPFN v2: competitive in some small-data settings, but runtime is high.
  - TabICL: best foundation-model tradeoff and best target for Big Plus.
  - Baseline caveat: tree models are fixed strong baselines, not tuned SOTA baselines.

## Slide 11: Limitations and Next Step

- Key message: The mainline is report-ready, and the Big Plus method is now frozen before new experiments.
- Suggested figure/table: Roadmap from method freezing to Adult smoke test.
- Speaker note bullets:
  - Mainline now covers metrics, runtime, scalability, and model tradeoffs.
  - Limitations: two datasets, classification only, repeated splits, mixed-device timing.
  - Full TabPFN v2 rows are constrained reference results beyond the cleaner 10k setting.
  - Big Plus remains TabICL support-set selection.
  - Phase 6 has frozen the support-set selection method before running new experiments.
  - Next step: implement the Adult experiment script and run a smoke test first.
