# 15 分钟展示中文版骨架

## Slide 1：项目标题

- 核心信息：本项目比较 tabular foundation models 与强树模型 baseline 在实际分类任务上的表现。
- 建议图表/表格：标题页，可放四个模型名和两个数据集名。
- 讲稿要点：
  - 介绍项目主题：tabular foundation models。
  - 说明主线模型：TabPFN v2、TabICL、LightGBM、XGBoost。
  - 说明主线数据集：Adult 和 Bank Marketing。
  - 强调本项目主线只做分类任务。

## Slide 2：研究动机

- 核心信息：tabular foundation models 很有潜力，但 boosted trees 仍然非常强且快。
- 建议图表/表格：foundation models vs tree baselines 的简短对比矩阵。
- 讲稿要点：
  - 表格数据在真实机器学习任务中非常常见。
  - boosted trees 是很可靠的表格 baseline。
  - foundation models 可能减少任务特定训练成本。
  - 本项目不只问“谁分数更高”，也问“什么情况下更好、代价是多少”。

## Slide 3：研究问题

- 核心信息：本项目关注预测质量、scalability 和 practical runtime。
- 建议图表/表格：三个评价维度的 bullet summary。
- 讲稿要点：
  - 在两个数据集上比较四个模型。
  - 使用 accuracy、balanced accuracy 和 macro-F1。
  - 研究 train size 从 512 到 full 时的变化。
  - 把 runtime 作为实用性指标一起分析。

## Slide 4：数据集与模型

- 核心信息：主线使用两个 OpenML 分类数据集和四个固定模型。
- 建议图表/表格：dataset/model setup table。
- 讲稿要点：
  - Adult 同时包含数值特征和类别特征。
  - Bank Marketing 类别不平衡更明显。
  - LightGBM 和 XGBoost 是 fixed strong baselines。
  - TabPFN v2 和 TabICL 是 foundation-model baselines。

## Slide 5：实验设置

- 核心信息：实验使用 repeated stratified splits 和固定主线设置。
- 建议图表/表格：实验流程图。
- 讲稿要点：
  - seeds 为 42、43、44、45、46。
  - 每个 seed 内，所有模型共享同一个 split。
  - 跨 seeds 是 repeated stratified splits，不是同一个固定测试集。
  - train-size grid 为 512、2048、8192、10000、full。
  - 不新增模型、不调参、不做 regression 或 survival analysis。

## Slide 6：Adult 主结果

- 核心信息：Adult 上树模型整体更强，TabICL 接近但没有明确超越。
- 建议图表/表格：从 `results/phase4_mainline_compare_summary.csv` 提取 Adult compact table。
- 讲稿要点：
  - XGBoost 在 `control_10k` 中 accuracy 最高。
  - LightGBM 在 Adult `control_10k` 中 balanced accuracy 和 macro-F1 最强。
  - TabICL 接近树模型。
  - TabPFN v2 指标较弱，并且 runtime 更高。

## Slide 7：Bank Marketing 主结果

- 核心信息：Bank Marketing 上 foundation models 更强，尤其 TabICL 在不平衡类别指标上更有优势。
- 建议图表/表格：从 `results/phase4_mainline_compare_summary.csv` 提取 Bank Marketing compact table。
- 讲稿要点：
  - TabICL 和 TabPFN v2 在 `control_10k` 中 accuracy 持平。
  - TabICL 在 balanced accuracy 和 macro-F1 上领先 TabPFN v2。
  - full-train reference 中，TabICL 在主要指标上整体领先。
  - 这个数据集说明只看 accuracy 不够。

## Slide 8：Train-Size Scalability

- 核心信息：更多训练数据通常提升指标，但提升幅度因数据集和模型而异。
- 建议图表/表格：`results/figures/phase5_scalability_macro_f1.png`。
- 讲稿要点：
  - Adult 上树模型从更大 train size 中收益更明显。
  - Bank Marketing 上所有模型的 macro-F1 都明显提升。
  - TabICL 在 Bank Marketing full train size 下 macro-F1 最高。
  - TabPFN v2 在 Adult 上提升较小，但 runtime 成本高。

## Slide 9：Runtime Scalability

- 核心信息：foundation models 的 runtime 随 train size 明显上升；TabICL 明显快于 TabPFN v2。
- 建议图表/表格：`results/figures/phase5_scalability_total_seconds_median.png`。
- 讲稿要点：
  - runtime 是 practical mixed-device timing。
  - 树模型在 CPU 上运行，并且仍然最快。
  - foundation models 可能使用 CUDA，所以这不是严格同设备公平速度比较。
  - 在较大 train size 下，TabICL 始终明显快于 TabPFN v2。

## Slide 10：模型优缺点

- 核心信息：最佳模型取决于数据集、指标和 runtime 预算。
- 建议图表/表格：四个模型的 pros/cons table。
- 讲稿要点：
  - LightGBM：快且强，尤其在 Adult 上。
  - XGBoost：快且有竞争力，Adult accuracy 很强。
  - TabPFN v2：小数据设置下有一定竞争力，但 runtime 高。
  - TabICL：foundation models 中 tradeoff 最好，也是 Big Plus 最合适入口。
  - baseline caveat：树模型是 fixed strong baselines，不是 tuned SOTA baselines。

## Slide 11：局限与下一步

- 核心信息：主线已经可以支撑报告；Big Plus 方法已在新实验前冻结。
- 建议图表/表格：从方法冻结到 Adult smoke test 的 roadmap。
- 讲稿要点：
  - 主线现在已经覆盖 metrics、runtime、scalability 和 model tradeoffs。
  - 局限包括：两个数据集、只做分类、repeated splits、mixed-device timing。
  - TabPFN v2 full rows 是超过更干净 10k 设置的 constrained reference results。
  - Big Plus 仍然是 TabICL support-set selection。
  - Phase 6 已先冻结方法，尚未运行新的完整 Big Plus 实验。
  - 下一步是实现 Adult 实验脚本，并先跑 smoke test。
