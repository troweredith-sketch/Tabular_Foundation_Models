# 表格基础模型与树模型 Baseline 在分类任务上的比较

## 标题

- 工作标题：中小型表格分类任务上 Tabular Foundation Models 与 Boosted-Tree Baselines 的比较
- 项目对象：在 Adult 和 Bank Marketing 上比较 TabPFN v2、TabICL、LightGBM 和 XGBoost。
- 主线贡献：在统一实验口径下，比较模型表现、类别不平衡指标、train-size scalability 和 practical runtime。

## 摘要草稿

- 本项目比较两个表格基础模型 TabPFN v2、TabICL 与两个强树模型 baseline：LightGBM 和 XGBoost。
- 实验使用两个 OpenML 分类数据集：Adult 和 Bank Marketing，并评估 accuracy、balanced accuracy、macro-F1 和 runtime。
- 实验采用 repeated stratified splits：每个 seed 内所有模型共享同一 split，但跨 seeds 不是同一个固定测试集。
- train-size scalability 覆盖 512、2048、8192、10000 和 full 五个训练规模。
- 结果显示，Adult 上树模型整体更强；Bank Marketing 上 foundation models 更有优势，尤其 TabICL 在不平衡类别指标上表现更好。
- runtime 分析显示，树模型明显更快；TabICL 明显快于 TabPFN v2；foundation models 的 runtime 随 train size 增大而明显上升。
- Big Plus ablation 进一步在 Adult 上研究 TabICL 支持集选择。冻结版本的 Balanced Prototype Retrieval 没有超过强随机 baseline，但预算受限支持集显著降低了 runtime。

## Introduction

- 表格数据在真实机器学习任务中非常常见，例如金融、营销、医疗和运营分析。
- Boosted-tree 方法仍然是表格预测任务中非常强的默认 baseline。
- Tabular foundation models 的价值在于可能减少任务特定训练，并通过预训练或 in-context learning 提供更通用的能力。
- 本项目关注一个实践问题：在本地统一实验条件下，tabular foundation models 什么时候比树模型更有优势？这种优势的运行成本是多少？
- 本项目只做分类任务，不扩展到 regression 或 survival analysis。
- 主要研究问题：
  - 在 Adult 和 Bank Marketing 上，哪类模型表现更好？
  - train size 增大时，accuracy、balanced accuracy 和 macro-F1 如何变化？
  - practical runtime 如何随 train size 变化？
  - 哪个模型最适合作为后续 Big Plus 的方法入口？
  - TabICL 支持集选择能否改善指标/runtime tradeoff？

## Related / Background

- Boosted-tree baselines：
  - LightGBM 和 XGBoost 是表格数据上常用且强力的 baseline。
  - 本项目中的 LightGBM 和 XGBoost 是 fixed strong baselines，不是 tuned SOTA baselines。
- Tabular foundation models：
  - TabPFN v2 是面向表格预测的 prior-data-fitted foundation model。
  - TabICL 更接近 in-context learning 视角，因此支持集选择天然适合作为后续 Big Plus 方向。
- 评价指标背景：
  - accuracy 容易理解，但在类别不平衡时可能掩盖少数类表现。
  - balanced accuracy 和 macro-F1 更适合补充分析 Bank Marketing 这类不平衡分类任务。
  - runtime 是模型实用性的重要组成部分，不能只看预测指标。

## Datasets

- Adult：
  - OpenML 表格分类数据集。
  - 同时包含数值特征和类别特征。
  - 主线观察：树模型仍然很强，TabICL 接近但没有明显超越 boosted trees。
- Bank Marketing：
  - OpenML 表格分类数据集，类别不平衡更明显。
  - 主线观察：foundation models 更有竞争力，TabICL 在不平衡类别指标上最突出。
- 两个数据集共同设置：
  - seeds 为 42、43、44、45、46。
  - 每个 seed 内，所有模型共享同一个 train/test split。
  - 跨 seeds 是 repeated stratified splits，不是同一个固定测试集。

## Models

- LightGBM：
  - 快速的 boosted-tree baseline。
  - Adult 上表现强，所有 train sizes 下 runtime 都很友好。
- XGBoost：
  - 快速且强力的 boosted-tree baseline。
  - Adult control_10k 中 accuracy 最高，但不是所有指标都最高。
- TabPFN v2：
  - foundation model baseline。
  - 小训练规模下有一定竞争力，但 runtime 高，尤其 full train size 下更明显。
  - full train-size 行超过更干净的 10k 支持范围口径，应作为 constrained reference results 呈现。
- TabICL：
  - 与 in-context support examples 天然相关的 foundation model。
  - Adult 上接近树模型，Bank Marketing 上不平衡类别指标最强。
  - 明显快于 TabPFN v2，因此是后续 Big Plus 的最佳入口。

## Experimental Setup

- 主线模型：
  - TabPFN v2
  - TabICL
  - LightGBM
  - XGBoost
- 主线数据集：
  - Adult
  - Bank Marketing
- 分类指标：
  - accuracy
  - balanced accuracy
  - macro-F1
- runtime 指标：
  - fit seconds
  - predict seconds
  - total seconds
- 主比较场景：
  - `control_10k`：使用 10000 条训练样本的更干净控制比较。
  - `full_train_reference`：使用完整训练集的工程参考线。
- scalability grid：
  - 512
  - 2048
  - 8192
  - 10000
  - full
- split caveat：
  - 实验使用 repeated stratified splits。
  - 每个 seed 内所有模型共享同一 split。
  - 跨 seeds 是重复抽样，不是同一个固定测试集。
- runtime caveat：
  - 树模型在 CPU 上运行。
  - foundation models 可能使用 CUDA。
  - 因此 runtime 是 practical mixed-device timing，不是严格同设备公平速度比较。
- baseline caveat：
  - LightGBM 和 XGBoost 是 fixed strong baselines，不是 tuned SOTA baselines。

## Main Results

- Adult：
  - `control_10k` 中，XGBoost 的 accuracy mean 最高，为 0.8698。
  - LightGBM 在 Adult `control_10k` 中的 balanced accuracy 和 macro-F1 最强。
  - TabICL 接近树模型，但没有明确超越。
  - TabPFN v2 在主线指标上较弱，并且明显慢于树模型。
- Bank Marketing：
  - `control_10k` 中，TabICL 和 TabPFN v2 的 accuracy mean 都是 0.9093。
  - TabICL 在 balanced accuracy 和 macro-F1 上强于 TabPFN v2。
  - `full_train_reference` 中，TabICL 在 accuracy、balanced accuracy 和 macro-F1 上都最高。
  - 树模型 runtime 仍明显更快，但预测指标不占优。
- 建议表格：
  - 从 `results/phase4_mainline_compare_summary.csv` 提取一张 compact main-results table。

## Scalability Analysis

- 建议图表：
  - `results/figures/phase5_scalability_accuracy.png`
  - `results/figures/phase5_scalability_balanced_accuracy.png`
  - `results/figures/phase5_scalability_macro_f1.png`
- Adult：
  - train size 增大时所有模型都有提升，但树模型收益更明显。
  - LightGBM 的 macro-F1 从 512 样本下的 0.7513 提升到 full 下的 0.8183。
  - TabPFN v2 在 Adult 上提升较小，仍低于最强 baseline。
- Bank Marketing：
  - train size 增大时，所有模型的 balanced accuracy 和 macro-F1 都明显提升。
  - TabICL 的 full-train macro-F1 最高，为 0.7745。
  - 这个数据集最能说明为什么不能只看 accuracy。

## Runtime Analysis

- 建议图表：
  - `results/figures/phase5_scalability_total_seconds_median.png`
- 树模型：
  - 在本地设置下通常保持在亚秒到约 1 秒量级。
  - practical efficiency 最强。
- TabPFN v2：
  - runtime 随 train size 明显上升。
  - 两个数据集 full-train total runtime 都在约 80 秒量级。
- TabICL：
  - runtime 也随 train size 上升，但 full-train runtime 约 20 到 22 秒。
  - 在保持指标竞争力的同时，明显快于 TabPFN v2。
- 解释：
  - runtime 支持后续 Big Plus 选择 TabICL，而不是 TabPFN v2。
  - 因为这是 mixed-device timing，结论应写成实际本地运行成本，而不是硬件归一化速度比较。

## Big Plus 支持集选择 Ablation

- 建议详细材料：
  - `report/phase6_big_plus_results_zh.md`
- 建议图表：
  - `results/figures/phase6_big_plus_adult_accuracy.png`
  - `results/figures/phase6_big_plus_adult_balanced_accuracy.png`
  - `results/figures/phase6_big_plus_adult_macro_f1.png`
  - `results/figures/phase6_big_plus_adult_total_seconds_median.png`
  - `results/figures/phase6_big_plus_adult_bpr_delta.png`
- 设置：
  - 数据集：只使用 Adult。
  - 模型：只使用 TabICL。
  - seeds：42、43、44。
  - budget-limited 支持集大小：512、2048、8192。
  - Full Context 使用当前 seed 下完整训练 split，是不受预算限制的参考线。
- 策略：
  - Full Context。
  - Random Subset。
  - Balanced Random Subset。
  - Balanced Prototype Retrieval。
- 主要结果：
  - Full Context 仍是总体最强参考：accuracy 0.8722，balanced accuracy 0.7919，macro-F1 0.8117。
  - Random Subset 在 accuracy 和 macro-F1 上是最强预算受限策略。
  - Balanced Random Subset 在 balanced accuracy 上最强。
  - Balanced Prototype Retrieval 在当前冻结的类中心原型定义下，没有超过两个随机 baseline。
- runtime：
  - Full Context median total runtime 为 45.8005 秒。
  - 预算受限策略大多在约 2.5 到 4.8 秒。
  - 支持集压缩对 runtime 有明确工程价值，但当前 BPR 规则没有带来预测指标收益。
- 解释：
  - 这一节应写成负结果 ablation，而不是成功方法。
  - 最重要的经验是：Balanced Random Subset 是任何后续 TabICL 检索方法必须击败的强 baseline。

## Discussion

- 模型表现依赖数据集。
  - Adult 更偏向 fixed boosted-tree baselines。
  - Bank Marketing 上 foundation models 优势更清楚。
- 不能只看 accuracy。
  - Bank Marketing 中 TabICL 与 TabPFN v2 accuracy 持平，但 balanced accuracy 和 macro-F1 不同。
- runtime 与预测指标之间有明显 tradeoff。
  - 树模型快且强。
  - TabICL 比树模型慢，但比 TabPFN v2 有更好的指标/runtime 平衡。
- Big Plus 动机：
  - TabICL 表现有竞争力，并且有可研究的 support-set structure。
  - 支持集选择是一个小而实的方法扩展，不改变主线范围。
- Big Plus 结果：
  - 冻结版 Adult 支持集选择实验给出了一个有价值的负结果。
  - 类中心 prototype selection 并不会自动比随机或类别平衡随机抽样更适合作为 TabICL 上下文。

## Limitations

- 主线只使用两个数据集。
- 只覆盖分类任务，不包括 regression 或 survival analysis。
- LightGBM 和 XGBoost 是 fixed strong baselines，不是 tuned SOTA baselines。
- runtime 是 practical mixed-device timing，不是严格同设备 timing。
- repeated stratified splits 意味着跨 seeds 的测试集不同。
- TabPFN v2 full train-size 行超过更干净的 10k 支持范围口径，应作为 constrained reference results。
- 没有做超参数调优，也没有额外模型搜索。
- Phase 6 Big Plus ablation 只覆盖 Adult 且只用 3 个 seeds，不能泛化成“检索式支持集选择一定无效”。

## Future Work

- 后续检索方法应该从 Phase 6 的负结果出发，而不是回改已经冻结的方法。
- 任何新支持集方法都应该在相同 budgets 和 splits 下明确超过 Random Subset 与 Balanced Random Subset。
- Bank Marketing 仍可以作为未来验证数据集，但当前 Phase 6 closure 没有启动它。
- 如果探索 boundary-aware retrieval 或 test-query-specific retrieval，应作为新的方法版本，而不是修改 Phase 6 冻结定义。

## Conclusion

- 当前主线已经足够独立支撑课程报告。
- 树模型仍然非常强，尤其在 Adult 和 runtime 上。
- foundation models 在 Bank Marketing 上更有价值，其中 TabICL 提供了最好的 foundation-model tradeoff。
- scalability 结果显示，train size 增大通常提升指标，但也增加 runtime，尤其对 foundation models 更明显。
- Phase 6 Adult Big Plus ablation 显示，支持集压缩可以降低 TabICL runtime，但冻结版 Balanced Prototype Retrieval 没有超过强随机 baseline。
