> Final source of truth: use report/report_draft.md, results/*.csv, and report/submission_manifest.md for the submitted results. This file may include historical planning or work-log context.

# Big Plus 规划：基于 TabICL 的检索式支持集选择改进

这份文档专门记录 Big Plus 轨道的正式定义。  
后续如果 Big Plus 的问题定义、方法设计、验证范围或优先级发生变化，优先更新这份文档。

## 1. Big Plus 在整个项目中的位置

这个项目现在分成两条轨道：

- `主线轨道`：完成课程项目主体比较
- `Big Plus 轨道`：提出一个比“直接跑现成模型”更进一步的方法性贡献

Big Plus 不是拿来替代主线的，而是在主线稳定之后，提供一个可以额外加分的小研究问题。

从 `2026-04-24` 起，Big Plus 的优先级顺延：它仍然保留为项目的重要加分方向，但不再是立即下一步。当前必须先完成主线硬要求闭环，包括补充 `balanced_accuracy`、`macro_f1`、train-size scalability、split protocol 修正、runtime caveat 和报告/PPT 骨架。只有这些内容完成后，才进入 Big Plus 实验阶段。

## 2. 为什么 Big Plus 选 TabICL

当前 Big Plus 固定围绕 `TabICL` 展开，而不是 `TabPFN v2`，原因有 3 个：

1. `TabICL` 天然更适合讨论“上下文样本怎么选”这个问题
2. 这个方向更接近项目文档里提到的“in-context learning strategies with retrieved examples”
3. 作为课程项目，它比微调路线更容易落地，同时比简单扩展任务类型更有方法创新味道

## 3. Big Plus 的核心问题

当前正式问题定义为：

> 在表格分类任务中，`TabICL` 的上下文支持集如果不是直接随机给定，而是通过更有代表性的检索式策略构造，是否能提升模型表现、稳定性或效率？

这句话里最关键的不是“要不要做检索”，而是：

- 支持集怎么选
- 为什么这种选择可能更好
- 这种改进是否只在一个数据集上有效

## 4. 方法边界

### 当前明确要做的内容

- 只做分类任务
- 只围绕 `TabICL`
- 只研究“支持集选择策略”
- 最终提交只采用 `Adult` 主深挖数据集；`Bank Marketing` 次验证保留为未来 Phase 7，不属于本次最终结果

### 当前明确不做的内容

- 不做回归任务
- 不做 survival analysis
- 不做模型微调或 adapter 训练
- 不做每个测试样本都重新动态检索的复杂系统
- 不把 Big Plus 写成一个泛泛的“多跑几个策略看看”

## 5. 数据集与验证范围

### 主深挖数据集

- `Adult`

作用：

- 用来完整定义 Big Plus 方法
- 用来做主要策略对比和分析
- 用来画图和写核心讨论

### 次验证数据集

- `Bank Marketing`

作用：

- 用来判断 Big Plus 是否只是 `Adult` 上的偶然现象
- 不重复完整消融，只验证最强方法
- 最终提交未执行该验证；它只作为未来 Phase 7 工作保留

### 备用数据集

- `Credit-G`

作用：

- 当 `Bank Marketing` 遇到技术阻塞时作为替代
- 或作为附录补充，而不是 Big Plus 主证据

## 6. 固定比较策略

Big Plus 从 `2026-04-26` 起采用方法冻结版本 `v1`。
除非后续单独记录为新版本，否则 Phase 6 Adult 主实验必须使用这里的定义，不能边跑边改。

Big Plus 固定比较以下 4 种支持集策略：

### `Full Context`

- 对每个 seed，使用该 seed 下完整训练 split 作为 `TabICL` 支持集
- 不做支持集抽样
- 不受 `512`、`2048`、`8192` 预算限制
- 作用是提供原始 `TabICL` 的 full-context reference

### `Random Subset`

- 对每个 seed 和预算 `B`，从训练 split 中随机无放回抽取 `B` 条样本
- 随机数使用当前实验 seed
- 如果 `B` 大于训练集大小，则使用全部训练样本
- 作用是提供最基础的预算受限 baseline

### `Balanced Random Subset`

- 对每个 seed 和预算 `B`，先按训练标签分配类别配额，再在每个类别内部随机无放回抽样
- 类别配额规则与 `Balanced Prototype Retrieval` 完全一致
- 随机数使用当前实验 seed
- 用来回答“性能变化是不是只是类别分布更均衡带来的”

### `Balanced Prototype Retrieval`

- 这是当前项目提出的方法
- 核心定义：在每个类别内部选择最接近本类别中心的代表性样本，再组成预算固定、类别尽量平衡的支持集
- 它不是每个测试样本动态检索一次，而是在每个 seed 和 budget 下先选出一个固定支持集

#### `Balanced Prototype Retrieval` 冻结细节

检索空间只用当前 seed 下的训练 split 构造。

- 数值特征：
  - 用训练 split 的 median 填补缺失值
  - 用训练 split 的 mean 和 standard deviation 标准化
  - 如果某列标准差为 `0`，实现时应让该列缩放后为 `0`
- 类别特征：
  - 用训练 split 的 most frequent 值填补缺失值
  - 用 `OneHotEncoder(handle_unknown="ignore")` one-hot 编码
  - 类别取值集合只从训练 split 学习
- 检索向量：
  - 定义如下：

$$
\mathbf{z}_i =
[
\mathrm{standardized\_numeric\_features}_i,\,
\mathrm{one\_hot\_categorical\_features}_i
]
$$

  - 该向量只用于选择支持集；被选中的原始样本仍交给 `TabICL` 使用其自身输入处理流程

距离度量固定为欧氏距离。
对每个类别 `c`，先计算类别中心：

$$
\boldsymbol{\mu}_c
=
\frac{1}{|\mathcal{I}_c|}
\sum_{i \in \mathcal{I}_c} \mathbf{z}_i,
\quad
\mathcal{I}_c = \{i : y_i = c\}
$$

每个训练样本的原型距离为：

$$
d_i
=
\left\lVert \mathbf{z}_i - \boldsymbol{\mu}_{y_i} \right\rVert_2
$$

类别配额规则固定如下，并同时用于 `Balanced Random Subset`：

1. 设类别数为 `K`，预算为 `B`，类别 `c` 的训练样本数为 `n_c`
2. 基础配额为 $\mathrm{base} = \left\lfloor B / K \right\rfloor$，每类先取 $q_c = \min(\mathrm{base}, n_c)$
3. 剩余预算 $R = B - \sum_{c \in C} q_c$
4. 对仍有剩余样本的类别，按训练集类别规模比例分配剩余预算
5. 如果比例分配后仍有余数，按最大小数余量补齐；并列时按训练集类别样本数多者优先，再按类别名排序保证确定性
6. 任一类别配额不能超过该类别训练样本数
7. 最终记录 `requested_budget` 和 `actual_support_size`

类别样本不足时：

- 该类别全部样本进入候选支持集
- 未使用的预算重新分配给仍有剩余样本的类别
- 不通过重复样本凑预算
- 如果所有训练样本都已用完，则允许 `actual_support_size < requested_budget`

原型选择规则：

- 在每个类别内部按 `d_i` 从小到大排序
- 选出该类别配额 `q_c` 个样本
- 距离完全相同时，用训练集原始行顺序做稳定 tie-break

信息边界：

- 只能使用训练 split 的特征和标签
- 不使用测试标签
- 不使用测试特征
- 不使用测试集类别比例
- 不根据测试集表现调整配额、距离度量或编码规则

与随机 baseline 的公平性：

- `Random Subset`、`Balanced Random Subset`、`Balanced Prototype Retrieval` 使用完全相同的 budgets：`512`、`2048`、`8192`
- 三者使用完全相同的 seeds：`42`、`43`、`44`
- 每个 seed 内三者共享同一个 stratified train/test split
- 同一 budget 下三者请求相同支持集大小
- 结果表必须记录 `strategy`、`seed`、`budget`、`requested_budget`、`actual_support_size` 和 `support_class_counts`

## 7. 当前方法假设

当前 Big Plus 的方法假设是：

- `TabICL` 并不是对所有上下文样本同样敏感
- 如果支持集里有更多“代表性强、覆盖更好、类别分布更稳”的样本，模型可能更容易利用上下文信息
- 即使准确率提升有限，这种选择策略也可能改善稳定性或在固定预算下更高效

## 8. 固定实验设置

### 前置条件

Big Plus 必须在主线硬要求闭环之后再运行。
如果 `accuracy` 之外的指标、scalability、split protocol、runtime caveat 和报告/PPT 骨架还没有完成，优先回到主线补强，不进入 Big Plus。

### 上下文预算

- `512`
- `2048`
- `8192`

### 随机种子

- `42`
- `43`
- `44`

### 评价维度

- `accuracy`
- `balanced_accuracy`
- `macro_f1`
- `fit_seconds`
- `predict_seconds`
- `total_seconds`
- 同一预算下的稳定性差异
- 是否存在明显失败模式

## 9. 主深挖阶段的预期产出

在 `Adult` 上，Big Plus 至少产出：

- 1 张“上下文预算 vs accuracy”图
- 1 张“上下文预算 vs balanced accuracy”图
- 1 张“上下文预算 vs macro-F1”图
- 1 张“上下文预算 vs runtime”图
- 1 张 4 种策略的 summary 对比表
- 1 张 `Balanced Prototype Retrieval` 相对随机 baseline 的 delta 表
- 1 张支持集类别构成检查表或图
- 1 节失败案例或负面结果分析

## 10. Future Phase 7 validation, not part of final submission

在 `Bank Marketing` 上的次验证没有进入最终提交。若未来启动 Phase 7，Big Plus 不再重复整套消融，只回答一个问题：

> 我们提出的检索式支持集选择方法，是否具有一定可迁移性？

因此次验证阶段只比较：

- 原始 `TabICL`
- 最强随机策略
- `Balanced Prototype Retrieval`
- 最强树模型 baseline

## 11. Pre-experiment Big Plus success criteria, retained as historical design notes

以下标准是实验前用于约束设计和判断结果价值的历史标准。最终 Phase 6 结果没有达到 performance-improving method 的标准；报告中将其解释为 negative ablation，而不是宣称 `Balanced Prototype Retrieval` 是成功的新方法。

实验前，满足下面任意一种，都可以认为 Big Plus 方向有提交价值：

### 情况 A：准确率提升

- 在主深挖数据集上，相比基础策略有稳定提升
- 在次验证数据集上至少没有完全失效

### 情况 B：稳定性或效率收益

- 准确率提升不大，但在固定预算下更稳定
- 或者在较小支持集预算下接近 `Full Context` 的效果

### 情况 C：有价值的负结果

- 方法没有带来提升
- 但能清楚说明为什么无效、失效发生在什么条件下、这说明了 `TabICL` 的什么特点

## 12. Big Plus 失败信号

下面这些情况说明 Big Plus 方向需要及时收缩，而不是继续硬耗：

- 主线硬要求尚未闭环，Big Plus 已经威胁最终交付
- `TabICL` 接入本身长期卡住，无法形成稳定主线
- 检索策略定义始终改来改去，无法形成固定方法
- 实验量过大，已经明显威胁主线结果完成
- 结果没有清晰故事，既讲不成“有效改进”，也讲不成“有价值的负结果”

## 13. 文档同步规则

只要 Big Plus 发生下面任意变化，就更新 `docs/big_plus_plan.md`：

- 问题定义变化
- 方法定义变化
- 验证数据集变化
- 对照策略变化
- 优先级变化

如果 Big Plus 完成一次真实实验，还要同步更新：

- `docs/experiment_log.md`
- `docs/work_log.md`
- `docs/project_record.md`
- 当前阶段对应的 `notebooks/phaseX_*.md`

## 14. 当前默认推进顺序

1. Phase 5 已完成：主线硬要求闭环与结果补强
2. Phase 6 已完成 Adult 主实验、结果图表和报告材料化
3. 当前优先继续最终报告正文、figure captions、结果表和展示材料整理
4. Phase 7 暂不启动；如未来启动，应作为新的验证步骤，而不是回改 Phase 6 冻结方法
5. 最后进入 Phase 8：整合英文报告、图表、PPT 和最终提交

## 15. 当前一句话版本

当前 Big Plus 可以概括成一句话：

> 我们不仅比较 tabular foundation models，还对 `TabICL` 支持集选择做了一个冻结版本 ablation；结果显示支持集压缩能显著降低 runtime，但当前 balanced prototype retrieval 没有超过强随机 baseline。
