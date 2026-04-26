# Comparing Tabular Foundation Models and Tree Baselines on Classification Tasks

## Title

- Working title: "Comparing Tabular Foundation Models and Boosted-Tree Baselines on Small-to-Medium Classification Tasks"
- Project focus: TabPFN v2, TabICL, LightGBM, and XGBoost on Adult and Bank Marketing.
- Main contribution: a controlled mainline comparison with additional imbalance-aware metrics, train-size scalability, and practical runtime analysis.

## Abstract Draft

- This project compares two tabular foundation models, TabPFN v2 and TabICL, against two strong boosted-tree baselines, LightGBM and XGBoost.
- The study uses two OpenML classification datasets, Adult and Bank Marketing, and evaluates accuracy, balanced accuracy, macro-F1, and runtime.
- Experiments use repeated stratified splits with shared model splits within each seed and train-size settings from 512 examples to full training data.
- Results show that tree baselines remain strongest on Adult, while foundation models, especially TabICL, are more competitive on Bank Marketing.
- Runtime results show a large practical cost gap: tree models are much faster, TabICL is substantially faster than TabPFN v2, and foundation model runtime grows sharply with train size.
- The Big Plus ablation explores TabICL support-set selection on Adult. The frozen balanced prototype retrieval rule does not beat strong random baselines, but budget-limited support sets substantially reduce runtime.

## Introduction

- Tabular data remains central in applied machine learning, especially in finance, marketing, healthcare, and operations.
- Boosted-tree methods are still strong default baselines for tabular prediction, but tabular foundation models promise broader reuse and in-context learning behavior.
- This project asks a practical question: under controlled local experiments, when do tabular foundation models look better than tree baselines, and what do they cost?
- The project scope is classification only; regression and survival analysis are intentionally out of scope.
- Main research questions:
  - Which model family performs best on Adult and Bank Marketing?
  - How do accuracy, balanced accuracy, and macro-F1 change with train size?
  - How does practical runtime scale with train size?
  - Which model is the best candidate for a small method extension?
  - Can TabICL support-set selection improve the metric/runtime tradeoff?

## Related / Background

- Boosted-tree baselines:
  - LightGBM and XGBoost are widely used strong tabular baselines.
  - In this project they are fixed strong baselines, not tuned SOTA baselines.
- Tabular foundation models:
  - TabPFN v2 is a prior-data-fitted foundation model for tabular prediction.
  - TabICL frames tabular prediction through an in-context learning style, making support-set selection a natural future extension.
- Evaluation background:
  - Accuracy is easy to interpret but can hide minority-class behavior.
  - Balanced accuracy and macro-F1 are useful complements for imbalanced classification, especially Bank Marketing.
  - Runtime matters because practical usability is part of the model tradeoff.

## Datasets

- Adult:
  - OpenML tabular classification dataset.
  - Mixes numerical and categorical features.
  - Main narrative: tree models remain very strong; TabICL is close but does not clearly beat boosted trees.
- Bank Marketing:
  - OpenML tabular classification dataset with stronger class imbalance.
  - Main narrative: foundation models are more competitive, and TabICL has the strongest imbalance-aware metrics.
- Both datasets:
  - Evaluated with repeated stratified splits over seeds 42, 43, 44, 45, and 46.
  - For each seed, models share the same train/test split.
  - Across seeds, the test set changes; this is not one single fixed test set reused for all seeds.

## Models

- LightGBM:
  - Fast boosted-tree baseline.
  - Strong on Adult and efficient across all train sizes.
- XGBoost:
  - Fast boosted-tree baseline.
  - Slightly highest Adult control_10k accuracy, but not strongest on all metrics.
- TabPFN v2:
  - Foundation model baseline.
  - Competitive at small train sizes but slow, especially at full train size.
  - Full train-size rows exceed the cleaner 10k support-range setting and should be treated as constrained reference results.
- TabICL:
  - Foundation model with a natural connection to in-context support examples.
  - Close to tree models on Adult and strongest overall on Bank Marketing imbalance-aware metrics.
  - Much faster than TabPFN v2, making it the best Big Plus entry point.

## Experimental Setup

- Mainline models: TabPFN v2, TabICL, LightGBM, and XGBoost.
- Mainline datasets: Adult and Bank Marketing.
- Classification metrics:
  - Accuracy.
  - Balanced accuracy.
  - Macro-F1.
- Runtime metrics:
  - Fit seconds.
  - Predict seconds.
  - Total seconds.
- Main comparison scenarios:
  - `control_10k`: cleaner controlled comparison with 10,000 training examples.
  - `full_train_reference`: engineering reference using full available training data.
- Scalability grid:
  - 512, 2048, 8192, 10000, and full.
- Split caveat:
  - Experiments use repeated stratified splits.
  - Within each seed, all models share the same split.
  - Across seeds, results are repeated splits rather than one fixed test set.
- Runtime caveat:
  - Tree models run on CPU.
  - Foundation models may use CUDA.
  - Runtime is practical mixed-device timing, not strict same-device benchmarking.
- Baseline caveat:
  - LightGBM and XGBoost are fixed strong baselines, not tuned SOTA baselines.

## Main Results

- Adult:
  - In `control_10k`, XGBoost has the highest accuracy mean at 0.8698.
  - LightGBM has the strongest Adult `control_10k` balanced accuracy and macro-F1.
  - TabICL is close to tree baselines but does not clearly outperform them.
  - TabPFN v2 is lower on the main metrics and much slower than tree models.
- Bank Marketing:
  - In `control_10k`, TabICL and TabPFN v2 tie on accuracy mean at 0.9093.
  - TabICL is stronger than TabPFN v2 on balanced accuracy and macro-F1.
  - In `full_train_reference`, TabICL has the best accuracy, balanced accuracy, and macro-F1.
  - Tree models remain much faster but do not lead the predictive metrics.
- Suggested table:
  - Use `results/phase4_mainline_compare_summary.csv` to create a compact main-results table.

## Scalability Analysis

- Suggested figures:
  - `results/figures/phase5_scalability_accuracy.png`
  - `results/figures/phase5_scalability_balanced_accuracy.png`
  - `results/figures/phase5_scalability_macro_f1.png`
- Adult:
  - Larger train sizes improve all models, but tree models benefit more clearly.
  - LightGBM macro-F1 rises from 0.7513 at 512 to 0.8183 at full.
  - TabPFN v2 improves less on Adult and remains below the strongest baselines.
- Bank Marketing:
  - Larger train sizes improve balanced accuracy and macro-F1 for all models.
  - TabICL reaches the strongest full-train macro-F1 at 0.7745.
  - The dataset shows why imbalance-aware metrics are important.

## Runtime Analysis

- Suggested figure:
  - `results/figures/phase5_scalability_total_seconds_median.png`
- Tree models:
  - Stay in the sub-second to roughly one-second range in this local setup.
  - Provide the strongest practical efficiency.
- TabPFN v2:
  - Runtime grows sharply with train size.
  - Full-train total runtime is around 80 seconds on both datasets.
- TabICL:
  - Runtime also grows with train size, but full-train runtime stays around 20 to 22 seconds.
  - Consistently much faster than TabPFN v2 while remaining competitive in metrics.
- Interpretation:
  - Runtime supports the project decision to use TabICL, not TabPFN v2, as the Big Plus target.
  - Because this is mixed-device timing, conclusions should be phrased as practical local cost rather than hardware-normalized speed.

## Big Plus Support-Set Selection Ablation

- Suggested detailed write-up:
  - `report/phase6_big_plus_results.md`
- Suggested figures:
  - `results/figures/phase6_big_plus_adult_accuracy.png`
  - `results/figures/phase6_big_plus_adult_balanced_accuracy.png`
  - `results/figures/phase6_big_plus_adult_macro_f1.png`
  - `results/figures/phase6_big_plus_adult_total_seconds_median.png`
  - `results/figures/phase6_big_plus_adult_bpr_delta.png`
- Setup:
  - Dataset: Adult only.
  - Model: TabICL only.
  - Seeds: 42, 43, and 44.
  - Budget-limited support sizes: 512, 2048, and 8192.
  - Full Context uses the complete seed-specific training split as a budget-independent reference.
- Strategies:
  - Full Context.
  - Random Subset.
  - Balanced Random Subset.
  - Balanced Prototype Retrieval.
- Main results:
  - Full Context remains strongest overall: accuracy 0.8722, balanced accuracy 0.7919, macro-F1 0.8117.
  - Random Subset is the strongest budget-limited strategy for accuracy and macro-F1.
  - Balanced Random Subset is strongest for balanced accuracy.
  - Balanced Prototype Retrieval does not outperform either random baseline under the frozen class-center prototype definition.
- Runtime:
  - Full Context median total runtime is 45.8005 seconds.
  - Budget-limited strategies mostly run in roughly 2.5 to 4.8 seconds.
  - Support-set compression is practically useful for runtime, even though this BPR rule does not improve predictive metrics.
- Interpretation:
  - This should be written as a negative ablation result, not as a successful method improvement.
  - The strongest lesson is that Balanced Random Subset is a hard baseline for any future TabICL retrieval method.

## Discussion

- Model performance is dataset-dependent.
  - Adult favors fixed boosted-tree baselines.
  - Bank Marketing gives foundation models a clearer advantage.
- Accuracy alone is insufficient.
  - On Bank Marketing, TabICL and TabPFN v2 tie in accuracy but differ in balanced accuracy and macro-F1.
- Runtime and metric performance trade off strongly.
  - Tree models are fast and strong.
  - TabICL is slower than trees but offers a better metric/runtime balance than TabPFN v2.
- Big Plus motivation:
  - TabICL is competitive and has a support-set structure that can be studied.
  - Support-set selection is a contained method extension that does not change the mainline scope.
- Big Plus outcome:
  - The frozen Adult support-set selection experiment gives a useful negative result.
  - Class-center prototype selection is not automatically a better context for TabICL than random or balanced random sampling.

## Limitations

- Only two mainline datasets are used.
- Only classification is covered; regression and survival analysis are out of scope.
- LightGBM and XGBoost are fixed strong baselines, not tuned SOTA baselines.
- Runtime is practical mixed-device timing, not strict same-device timing.
- Repeated stratified splits change the test set across seeds.
- Full train-size TabPFN v2 rows exceed the cleaner 10k support-range setting and should be presented as constrained reference results.
- No hyperparameter tuning or additional model search is included.
- The Phase 6 Big Plus ablation is Adult-only and uses only three seeds, so it should not be generalized as a universal failure of retrieval-based support selection.

## Future Work

- Future retrieval work should start from the Phase 6 negative result rather than retrofitting the frozen method.
- Any new support-set method should explicitly beat both Random Subset and Balanced Random Subset under the same budgets and splits.
- Bank Marketing remains a possible later validation dataset, but it was not launched as part of the current Phase 6 closure.
- Potential method changes, such as boundary-aware retrieval or test-query-specific retrieval, should be treated as new method versions rather than edits to the frozen Phase 6 definition.

## Conclusion

- The mainline comparison is now complete enough to stand alone as a course report.
- Tree baselines remain very strong, especially on Adult and runtime.
- Foundation models show more value on Bank Marketing, with TabICL providing the strongest overall foundation-model tradeoff.
- Scalability results show that train size improves metrics but increases runtime, especially for foundation models.
- The Phase 6 Adult Big Plus ablation shows that support-set compression can reduce TabICL runtime, but the frozen balanced prototype retrieval rule does not improve predictive performance over strong random baselines.
