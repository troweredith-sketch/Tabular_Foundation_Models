# Phase 6 Big Plus 结果整理：Adult 上的 TabICL 支持集选择

## 目的

Phase 6 研究一个围绕 `TabICL` 的小型 Big Plus 扩展：在不换模型、不新增模型、不调参的前提下，改变支持集选择方式是否能改善指标或 runtime tradeoff。

这一步是 Adult 数据集上的支持集选择 ablation。它不应该被写成“新方法成功”，而应该被写成一次冻结方法后的诚实验证：当前 `Balanced Prototype Retrieval` 没有超过强随机 baseline。

## 实验设置

- 数据集：Adult。
- 模型：`TabICL`。
- seeds：`42`, `43`, `44`。
- 划分方式：repeated stratified splits；同一个 seed 内所有策略共享同一 split。
- budget-limited 支持集大小：`512`, `2048`, `8192`。
- 完整参考支持集：`Full Context`，使用当前 seed 下完整训练 split，共 `39073` 条。
- 指标：accuracy、balanced accuracy、macro-F1，以及支持集构造完成之后的 TabICL fit+predict runtime。

四种策略：

- `Full Context`：完整训练 split，作为不受预算限制的参考线。
- `Random Subset`：从训练 split 中随机无放回抽取指定 budget。
- `Balanced Random Subset`：先按类别配额分配 budget，再在类内随机抽样。
- `Balanced Prototype Retrieval`：使用同一套类别配额，在 train-only 检索空间中选择最接近类别中心的样本。

## 结果表

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

## 解释

冻结版本的 `Balanced Prototype Retrieval` 没有优于两个随机 baseline。
它在所有 budget 和所有指标上都低于 `Balanced Random Subset`。
相对 `Random Subset`，它只有在 `budget=2048` 的 balanced accuracy 上有一个极小正差值（`+0.0016`），但 accuracy 和 macro-F1 仍明显更低。

budget-limited 策略的表现可以这样写：

- `Random Subset` 在 accuracy 和 macro-F1 上更稳，且随着 budget 增大接近 `Full Context`。
- `Balanced Random Subset` 在 balanced accuracy 上最强，说明类别平衡本身是一个强 baseline。
- `Balanced Prototype Retrieval` 在当前“类中心原型”冻结定义下不具竞争力。

runtime 结果仍然有价值，但它是模型侧计时：

- 表中 runtime 只统计支持集构造完成之后的 TabICL fit+predict 时间，不包括 BPR preprocessing、class-center 计算或 distance ranking。
- `Full Context` 的 median TabICL fit+predict runtime 为 `45.8005s`。
- 三种 budget-limited 策略大致在 `2.5s` 到 `4.8s`。
- 这说明支持集压缩能显著降低 `TabICL` 的模型执行成本，但当前 BPR 规则没有把效率收益转化为性能收益。

## 图表引用

- `results/figures/phase6_big_plus_adult_accuracy.png`
- `results/figures/phase6_big_plus_adult_balanced_accuracy.png`
- `results/figures/phase6_big_plus_adult_macro_f1.png`
- `results/figures/phase6_big_plus_adult_total_seconds_median.png`
- `results/figures/phase6_big_plus_adult_bpr_delta.png`

建议 caption：

- Accuracy vs support budget：Random Subset 随 budget 增大逐渐接近 Full Context；冻结版 BPR 明显落后。
- Balanced accuracy vs support budget：Balanced Random Subset 是最强 budget-limited 策略，说明类别平衡本身就是强 baseline。
- Macro-F1 vs support budget：Random Subset 更稳定，BPR 没有缩小差距。
- Runtime by support budget：三种 budget-limited 策略都远快于 Full Context，支持集压缩有明确工程价值。
- BPR delta：BPR 相对两个随机 baseline 主要为负，应作为负结果呈现。

## 可直接写进报告的表述

建议表述：

> 作为 Big Plus ablation，我们测试了改变 `TabICL` 支持集选择方式是否能改善 Adult 结果。冻结版本的 balanced prototype retrieval 没有超过随机 baseline。Random Subset 在 accuracy 和 macro-F1 上更强，Balanced Random Subset 在 balanced accuracy 上最好。不过，所有预算受限支持集都显著降低了 runtime，说明支持集压缩对效率有价值，但“选择靠近类别中心的原型样本”不足以在当前设置下提升预测性能。

避免表述：

- “Balanced Prototype Retrieval 提升了 TabICL。”
- “Big Plus 方法在 Adult 上成功。”
- “原型检索优于随机抽样。”

更准确的结论是：当前冻结版 BPR 是一个有价值的负结果；后续任何检索方法都需要明确击败 `Balanced Random Subset` 这个强 baseline。
