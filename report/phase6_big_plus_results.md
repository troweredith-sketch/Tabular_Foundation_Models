# Phase 6 Big Plus Results: TabICL Support-Set Selection on Adult

## Purpose

Phase 6 studies a small Big Plus extension around `TabICL`: whether changing the support set can improve the metric/runtime tradeoff without changing the model, adding new models, or tuning hyperparameters.

This is an ablation on the Adult dataset only. It should not be presented as a new winning method. The main value is to show what happens when a frozen support-set selection idea is tested against strong random baselines.

## Experimental Setting

- Dataset: Adult.
- Model: `TabICL`.
- Seeds: `42`, `43`, `44`.
- Split protocol: repeated stratified splits; all strategies share the same split within each seed.
- Budget-limited support sizes: `512`, `2048`, `8192`.
- Reference support size: `Full Context`, using the full seed-specific training split of `39073` examples.
- Metrics: accuracy, balanced accuracy, macro-F1, and TabICL fit+predict runtime after support-set construction.

Strategies:

- `Full Context`: use the complete training split as a budget-independent reference.
- `Random Subset`: sample the requested budget uniformly without replacement.
- `Balanced Random Subset`: allocate the budget by class quota, then sample randomly within class.
- `Balanced Prototype Retrieval`: allocate the same class quotas as balanced random, then choose class-center prototypes in a train-only retrieval space.

## Result Summary

| Strategy | Budget | Accuracy | Balanced Accuracy | Macro-F1 | Median TabICL Fit+Predict Seconds |
| --- | ---: | ---: | ---: | ---: | ---: |
| Full Context | full | 0.8722 | 0.7919 | 0.8117 | 45.8005 |
| Random Subset | 512 | 0.8438 | 0.7358 | 0.7592 | 3.4771 |
| Random Subset | 2048 | 0.8573 | 0.7668 | 0.7873 | 2.5291 |
| Random Subset | 8192 | 0.8654 | 0.7874 | 0.8038 | 4.6601 |
| Balanced Random Subset | 512 | 0.7964 | 0.8180 | 0.7610 | 3.4701 |
| Balanced Random Subset | 2048 | 0.8155 | 0.8295 | 0.7792 | 2.5361 |
| Balanced Random Subset | 8192 | 0.8344 | 0.8293 | 0.7941 | 4.6720 |
| Balanced Prototype Retrieval | 512 | 0.7020 | 0.7093 | 0.6588 | 3.2666 |
| Balanced Prototype Retrieval | 2048 | 0.7336 | 0.7684 | 0.7002 | 2.4829 |
| Balanced Prototype Retrieval | 8192 | 0.6437 | 0.7256 | 0.6253 | 4.7904 |

## Interpretation

The frozen `Balanced Prototype Retrieval` version does not outperform the random baselines. It is lower than `Balanced Random Subset` on every metric and every budget. Against `Random Subset`, it only has a very small positive balanced-accuracy delta at budget `2048` (`+0.0016`), while accuracy and macro-F1 remain clearly lower.

The strongest budget-limited behavior is split by metric:

- `Random Subset` is strongest for accuracy and macro-F1.
- `Balanced Random Subset` is strongest for balanced accuracy.
- `Balanced Prototype Retrieval` is not competitive under the frozen class-center prototype definition.

The runtime result is still useful, but it is model-side timing: the column measures TabICL fit+predict time after support-set construction and does not include BPR preprocessing, class-center computation, or distance ranking. Under that definition, budget-limited support sets reduce median runtime from `45.8005s` for `Full Context` to roughly `2.5s` to `4.8s`. This supports the narrower claim that support-set compression can make TabICL model execution more practical, even though this specific retrieval rule did not improve predictive metrics.

## Figure References

- `results/figures/phase6_big_plus_adult_accuracy.png`
- `results/figures/phase6_big_plus_adult_balanced_accuracy.png`
- `results/figures/phase6_big_plus_adult_macro_f1.png`
- `results/figures/phase6_big_plus_adult_total_seconds_median.png`
- `results/figures/phase6_big_plus_adult_bpr_delta.png`

Suggested captions:

- Accuracy vs support budget: random subset approaches the full-context reference as the budget grows, while the frozen prototype retrieval strategy remains substantially lower.
- Balanced accuracy vs support budget: balanced random subset is the strongest budget-limited strategy, showing that class balancing itself is a strong baseline.
- Macro-F1 vs support budget: random subset remains the most stable budget-limited strategy, and balanced prototype retrieval does not close the gap.
- Runtime by support budget: all budget-limited strategies are much faster than full context, so support-set compression is practically useful even without a retrieval gain.
- BPR delta: the frozen BPR strategy is mostly negative relative to both random baselines; it should be reported as a negative ablation result.

## Report Wording

Recommended wording:

> As a Big Plus ablation, we tested whether selecting a more representative `TabICL` support set improves the Adult results. The frozen balanced prototype retrieval strategy did not outperform the random baselines. Random subset was stronger for accuracy and macro-F1, while balanced random subset was strongest for balanced accuracy. However, all budget-limited support sets substantially reduced runtime compared with full context. This suggests that support-set compression is useful for efficiency, but class-center prototype selection is not sufficient as a performance-improving retrieval rule in this setting.

Avoid wording such as:

- "Balanced Prototype Retrieval improves TabICL."
- "The Big Plus method succeeds on Adult."
- "Prototype retrieval beats random sampling."

The honest conclusion is narrower: this frozen BPR version is a useful negative result, and `Balanced Random Subset` is a strong baseline that future retrieval methods must beat.
