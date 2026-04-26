# Phase 6：Big Plus 方法冻结与 Adult 主实验分析

这篇文档是 Phase 6 的学习型 notebook。
当前记录 Phase 6 的三个步骤：

1. 冻结 `TabICL` 支持集选择 Big Plus 方法，并设计后续 `Adult` 主实验。
2. 实现 `src/phase6_big_plus_adult.py`，并完成 `budget=512, seed=42` 的 smoke test。
3. 完成 `Adult` 主实验，并生成结果分析图。

完整 Adult 主实验已经完成。
当前正式结论基于 `results/phase6_big_plus_adult.csv` 和 `results/phase6_big_plus_adult_summary.csv`。
早期 smoke test 记录保留在第 12 节，只作为工程历史，不作为最终结论。

## 0. Adult 主实验结论快照

本次主实验只覆盖 `Adult`，没有启动 `Bank Marketing` 次验证，也没有重跑 Phase 4/5 主线。

实验设置：

- dataset：`adult`
- model：`TabICL`
- seeds：`42`, `43`, `44`
- budget-limited budgets：`512`, `2048`, `8192`
- strategies：`full_context`, `random_subset`, `balanced_random_subset`, `balanced_prototype_retrieval`

验收结果：

- `results/phase6_big_plus_adult.csv`：`30` 行
- `results/phase6_big_plus_adult_summary.csv`：`10` 行
- 两个 CSV 都包含 `requested_budget`、`actual_support_size`、`support_class_counts`
- 三个 budget-limited 策略在同一 `budget/seed` 下 `requested_budget` 一致
- 所有运行均使用 `cuda`

核心发现：

- `Full Context` 仍是总体最强参照：accuracy `0.8722`，macro-F1 `0.8117`。
- `Random Subset` 在 accuracy 和 macro-F1 上最稳，随预算增大接近 `Full Context`。
- `Balanced Random Subset` 在 balanced accuracy 上最好，三个预算均高于 `Random Subset` 和 `BPR`。
- `Balanced Prototype Retrieval` 没有优于两个随机 baseline；只有 `budget=2048` 的 balanced accuracy 比 `Random Subset` 高 `0.0016`，但 accuracy 和 macro-F1 更低。
- runtime 符合预期：budget-limited 策略 median runtime 约 `2.48s` 到 `4.79s`，明显低于 `Full Context` 的 `45.80s`。

生成图表：

- `results/figures/phase6_big_plus_adult_accuracy.png`
- `results/figures/phase6_big_plus_adult_balanced_accuracy.png`
- `results/figures/phase6_big_plus_adult_macro_f1.png`
- `results/figures/phase6_big_plus_adult_total_seconds_median.png`
- `results/figures/phase6_big_plus_adult_bpr_delta.png`

## 1. 阶段目标

Phase 6 的目标是把 Big Plus 从“一个想法”变成“一个固定可复现的实验设计”。

当前固定问题是：

> 在表格分类任务中，如果 `TabICL` 的上下文支持集不是简单使用全部训练集或随机抽样，而是用更有代表性的策略选择，是否能在固定支持集预算下提升表现、稳定性或效率？

这一步只冻结方法定义，不启动完整长实验。

保持不变的项目边界是：

- 不新增模型
- 不调参
- 不扩展到 regression
- 不扩展到 survival analysis
- 不重新跑 Phase 4/5 主线实验
- Big Plus 仍然只围绕 `TabICL` 的支持集选择

## 2. 这一阶段做了什么

本次完成的是 Phase 6 第一步：方法冻结和实验设计。

具体完成内容包括：

- 固定 Big Plus 的四种支持集策略
- 明确 `Balanced Prototype Retrieval` 的检索空间和选择规则
- 固定主数据集、次验证数据集、预算和 seeds
- 明确哪些信息可以使用，哪些信息不能使用
- 设计后续 Adult 主实验应该输出的结果表和图
- 记录当前风险，避免把未完成实验写成已经完成

方法冻结时没有运行新的 `TabICL` 实验。
后续已完成一次 smoke test，用于确认脚本实现和结果表结构。

## 3. 关键概念学习

### 3.1 什么是支持集

在这个项目里，支持集可以理解为 `TabICL` 在预测时看到的上下文样本。
如果支持集不同，模型接收到的上下文信息就不同，预测结果也可能改变。

所以 Big Plus 的问题不是“换一个模型”，而是问：

> 同一个 `TabICL`，给它不同方式选出来的上下文样本，会不会更好？

### 3.2 为什么先冻结方法

如果在实验过程中不断修改支持集策略，就会出现一个问题：

> 结果好时不知道是方法真的有效，还是因为我们根据结果调过方法。

所以 Phase 6 第一步必须先冻结策略。
之后即使结果不好，也应该先按冻结版本解释，而不是立即改方法追分数。

### 3.3 预算是什么意思

支持集预算指的是允许放进 `TabICL` 上下文里的训练样本数量。

当前固定预算是：

- `512`
- `2048`
- `8192`

这些预算只用于预算受限的三种策略：

- `Random Subset`
- `Balanced Random Subset`
- `Balanced Prototype Retrieval`

`Full Context` 是不受预算限制的参照线，直接使用当前 seed 下的完整训练集。
在图里它更适合作为一条 `full` 参考线，而不是和 `512/2048/8192` 混在同一个预算含义里。

## 4. 四种支持集策略

### 4.1 Full Context

`Full Context` 是原始参照策略。

定义：

- 对每个 seed，先做和主线一致的 stratified train/test split
- 使用该 seed 下完整训练集作为 `TabICL` 支持集
- 不做支持集抽样
- 不受 `512/2048/8192` 预算限制

作用：

- 作为“没有压缩支持集”的工程参照线
- 帮助判断小预算策略是否接近完整训练集效果

注意：

- 它不是预算公平 baseline
- 预算公平比较主要发生在另外三种策略之间

### 4.2 Random Subset

`Random Subset` 是最基础的预算 baseline。

定义：

- 对每个 seed 和预算 `B`
- 从当前训练 split 中随机无放回抽取 `B` 条样本
- 如果 `B` 大于训练集大小，则使用全部训练样本
- 随机数使用当前实验 seed

作用：

- 回答“只减少支持集大小会发生什么”
- 给检索方法提供最基础的对照

它不主动使用类别平衡信息，所以抽样后的类别比例只是在期望上接近原训练集比例。

### 4.3 Balanced Random Subset

`Balanced Random Subset` 是类别平衡的随机 baseline。

定义：

- 对每个 seed 和预算 `B`
- 先根据训练标签分配每个类别的预算配额
- 再在每个类别内部随机无放回抽样
- 随机数使用当前实验 seed

作用：

- 回答“提升是否只是因为类别更平衡”
- 和 `Balanced Prototype Retrieval` 使用同一套类别配额规则

如果 `Balanced Prototype Retrieval` 优于 `Random Subset`，但不优于 `Balanced Random Subset`，说明收益可能主要来自类别平衡，而不是原型检索本身。

### 4.4 Balanced Prototype Retrieval

`Balanced Prototype Retrieval` 是当前 Big Plus 的方法策略。

它的核心想法是：

> 在每个类别内部，选择最接近本类别中心的代表性样本，再把这些样本组成预算固定、类别尽量平衡的支持集。

这个方法不是每个测试样本动态检索一次。
它是在每个 seed 和预算下，先从训练集里选出一个固定支持集，然后用这同一个支持集预测该 seed 的测试集。

## 5. Balanced Prototype Retrieval 冻结定义

### 5.1 检索空间如何构造

检索空间只用当前 seed 下的训练 split 构造。

对训练集特征做两类转换：

- 数值特征：
  - 用训练集数值列的 median 做缺失值填补
  - 用训练集数值列的 mean 和 standard deviation 做标准化
  - 标准化后的每个数值特征进入检索向量
- 类别特征：
  - 用训练集类别列的 most frequent 值做缺失值填补
  - 用 `OneHotEncoder(handle_unknown="ignore")` 做 one-hot 编码
  - 类别取值集合只从训练集学习

最终检索向量是：

```text
z_i = [standardized_numeric_features_i, one_hot_categorical_features_i]
```

这个检索向量只用于选择支持集。
被选中的原始样本仍然交给 `TabICL` 使用它自己的输入处理流程。

### 5.2 数值特征如何标准化

数值特征标准化规则固定为：

```text
x_scaled = (x_imputed - train_mean) / train_std
```

其中：

- `x_imputed` 是用训练集 median 填补后的数值特征
- `train_mean` 只在训练 split 上计算
- `train_std` 只在训练 split 上计算

如果某个数值列在训练 split 中标准差为 `0`，实现时应让该列缩放后为 `0`，避免除零。
这类列对欧氏距离没有区分能力。

### 5.3 类别特征如何 one-hot

类别特征 one-hot 规则固定为：

- 类别缺失值先用训练 split 的 most frequent 值填补
- one-hot 类别表只从训练 split 拟合
- 未在训练 split 出现的类别不参与检索空间
- `handle_unknown="ignore"` 只作为实现保险

因为 `Balanced Prototype Retrieval` 不使用测试特征构造检索空间，所以正常情况下不会在检索阶段遇到测试集未知类别。

### 5.4 距离度量

距离度量固定为欧氏距离。

对每个类别 `c`，先计算该类别在检索空间中的中心：

```text
mu_c = mean(z_i for training samples i with y_i = c)
```

每个训练样本的原型距离为：

```text
d_i = ||z_i - mu_{y_i}||_2
```

也就是说，一个样本越接近自己类别的中心，就越被认为是该类别的代表性原型。

### 5.5 类别配额分配规则

对预算 `B` 和类别集合 `C`，固定使用同一套配额规则。
这套规则同时用于：

- `Balanced Random Subset`
- `Balanced Prototype Retrieval`

规则如下：

1. 设类别数为 `K`，每类训练样本数为 `n_c`
2. 先给每个类别基础配额：

```text
base = floor(B / K)
q_c = min(base, n_c)
```

3. 计算剩余预算：

```text
R = B - sum(q_c)
```

4. 对仍有剩余样本的类别，按训练集类别规模比例分配剩余预算
5. 如果比例分配后仍有余数，按最大小数余量补齐；并列时按训练集类别样本数多者优先，再按类别名排序保证确定性
6. 任一类别配额不能超过该类别训练样本数
7. 最终支持集大小应尽量等于 `B`

在 Adult 和 Bank Marketing 的当前预算下，正常情况下每个预算都能被填满。
但实现时仍应记录 `requested_budget` 和 `actual_support_size`，方便发现异常。

### 5.6 类别样本不足时如何处理

如果某个类别训练样本数少于它的目标配额：

- 该类别全部样本进入候选支持集
- 没用完的预算重新分配给还有剩余样本的类别
- 重新分配仍按训练集类别规模比例进行
- 如果所有类别都已经用完，则 `actual_support_size < requested_budget`

这个规则保证方法不会因为少数类样本不足而报错，也不会通过重复样本来凑预算。

### 5.7 如何选择原型样本

在每个类别内部：

1. 计算该类别每个样本到本类别中心 `mu_c` 的欧氏距离
2. 按距离从小到大排序
3. 选出该类别配额 `q_c` 个样本
4. 如果距离完全相同，用训练集原始行顺序做稳定 tie-break

这个选择过程是确定性的。
`Balanced Prototype Retrieval` 使用 seed 的方式主要体现在 train/test split 上，而不是额外随机抽样上。

### 5.8 是否允许使用测试信息

不允许。

冻结规则是：

- 不使用测试标签
- 不使用测试特征
- 不使用测试集类别比例
- 不根据测试集表现调整配额、距离度量或编码规则
- 不对每个测试样本做动态 nearest-neighbor 检索

可以使用的信息只有：

- 当前 seed 下训练 split 的特征
- 当前 seed 下训练 split 的标签
- 预先固定的 budget 和 seed

### 5.9 如何保证和随机 baseline 使用相同 budget 和 seeds

所有预算受限策略都使用同一组设置：

- 数据集：`Adult`
- budgets：`512`, `2048`, `8192`
- seeds：`42`, `43`, `44`
- split：每个 seed 内共享同一个 stratified train/test split
- requested budget：同一 budget 下三种预算策略都请求相同支持集大小

三种预算策略的区别只在支持集选择规则：

- `Random Subset`：全训练集随机抽样
- `Balanced Random Subset`：按类别配额后类内随机抽样
- `Balanced Prototype Retrieval`：按类别配额后类内选最近类别中心的原型样本

实现时应该在结果表中记录：

- `seed`
- `budget`
- `requested_budget`
- `actual_support_size`
- `support_class_counts`
- `strategy`

这样后续可以检查是否真的做到了预算一致。

## 6. 为什么这样设计

这套设计的重点是控制变量。

`Random Subset` 控制的是“随机抽固定数量支持集”的基础效果。
`Balanced Random Subset` 控制的是“类别平衡”本身带来的效果。
`Balanced Prototype Retrieval` 在此基础上再加入“代表性原型”这个方法假设。

所以后续解读时要按下面顺序问：

1. 小预算策略能不能接近 `Full Context`
2. 类别平衡是否比完全随机更稳
3. 原型检索是否比类别平衡随机更好
4. 如果没有更好，它的失败模式是什么

这样即使结果不是正向提升，也能形成有价值的负结果分析。

## 7. Phase 6 Adult 主实验设计

### 7.1 数据集

主实验数据集固定为：

- `Adult`

次验证数据集保留为：

- `Bank Marketing`

本阶段只设计 Adult 主实验，不提前启动 Bank Marketing 次验证。

### 7.2 模型

只使用：

- `TabICL`

不新增模型。
不重新比较 `TabPFN v2`、`LightGBM`、`XGBoost`。

### 7.3 Seeds

当前冻结 seeds 为：

- `42`
- `43`
- `44`

每个 seed 内，四种策略共享同一个 train/test split。
跨 seeds 是 repeated stratified splits。

### 7.4 Budgets

预算受限策略固定使用：

- `512`
- `2048`
- `8192`

`Full Context` 使用完整训练集，作为 budget-independent reference。

### 7.5 指标

为了和主线口径保持一致，Phase 6 至少记录：

- `accuracy`
- `balanced_accuracy`
- `macro_f1`
- `fit_seconds`
- `predict_seconds`
- `total_seconds`

额外记录支持集相关字段：

- `strategy`
- `budget`
- `requested_budget`
- `actual_support_size`
- `support_class_counts`
- `seed`
- `split`

## 8. 预期输出

### 8.1 结果表

Adult 主实验应该至少生成三类表。

第一类是 detail 表：

- 每一行是一组 `seed + strategy + budget` 的结果
- `Full Context` 可以使用 `budget = full`
- 预算受限策略使用 `512/2048/8192`

建议文件名：

- `results/phase6_big_plus_adult.csv`

第二类是 summary 表：

- 按 `strategy + budget` 聚合
- 记录 `n_runs`
- 记录 `seeds`
- 对 `accuracy`、`balanced_accuracy`、`macro_f1` 计算 mean/std/min/max
- 对 runtime 计算 median

建议文件名：

- `results/phase6_big_plus_adult_summary.csv`

第三类是差值表：

- 计算 `Balanced Prototype Retrieval` 相对随机 baseline 的差值
- 至少包含：
  - BPR - Random Subset
  - BPR - Balanced Random Subset

建议文件名：

- `results/phase6_big_plus_adult_deltas.csv`

### 8.2 图表

Adult 主实验应该至少生成以下图。

第一组：预算 vs 指标

- `budget vs accuracy`
- `budget vs balanced_accuracy`
- `budget vs macro_f1`
- 图中给出 mean，最好带 seed 间误差条或标准差阴影
- `Full Context` 作为水平参考线

第二组：预算 vs runtime

- `budget vs total_seconds`
- 可补 `budget vs predict_seconds`
- y 轴可以使用 log-scale，方便同时看小预算和大预算

第三组：稳定性或差值图

- `Balanced Prototype Retrieval` 相对两个随机 baseline 的 metric delta
- 或者展示不同 seeds 下的点图

第四组：支持集构成检查图

- 不同策略、不同 budget 下的类别比例
- 用来确认 balanced 策略是否真的按预期控制类别配额

建议输出目录：

- `results/figures/`

## 9. 当前结果说明了什么

当前还没有 Phase 6 完整 Adult 主实验结果。
已经有一次 `budget=512, seed=42` 的 smoke test 结果，但它只用于确认脚本和结果 schema，不用于正式判断方法有效性。

所以现在只能说：

- Big Plus 方法定义已经冻结
- Adult 主实验设计已经明确
- 结果表和图表目标已经明确
- Phase 6 Adult 脚本已经实现
- smoke test 已确认四种策略都能运行并写出 CSV

不能说：

- `Balanced Prototype Retrieval` 已经提升了 accuracy
- Big Plus 已经在 Adult 上成功
- 该方法已经能迁移到 Bank Marketing

这些都需要后续真实实验结果支持。

## 10. 遇到的问题与风险

### 10.1 Full Context 与预算策略不完全公平

`Full Context` 使用完整训练集，不受 `512/2048/8192` 预算限制。

处理方式：

- 把它写成 reference，不写成预算公平 baseline
- 图中用水平线或单独 `full` 点表示
- 主要预算公平比较放在三种预算策略之间

### 10.2 原型样本可能过于中心化

选择最接近类别中心的样本可能会忽略边界样本。
如果 `TabICL` 需要边界信息，原型检索未必更好。

处理方式：

- 先不改方法
- 如果结果不好，把它写成失败模式
- 不在 Phase 6 运行后临时改成边界检索

### 10.3 One-hot 维度可能影响距离

类别特征 one-hot 后可能维度较高，欧氏距离会受到类别特征数量影响。

处理方式：

- 本冻结版本不额外加权数值/类别特征
- 把它记录为限制
- 不在主实验中调距离权重

### 10.4 类别配额可能改变原始分布

Balanced 策略会让支持集类别比例比原训练集更均衡。
这既可能帮助少数类，也可能损失总体 accuracy。

处理方式：

- 同时看 `accuracy`、`balanced_accuracy`、`macro_f1`
- 用 `Balanced Random Subset` 判断收益是否来自类别平衡

### 10.5 实验量仍然需要控制

Adult 主实验的预算受限部分是：

```text
3 strategies × 3 budgets × 3 seeds = 27 runs
```

加上 `Full Context`：

```text
3 seeds = 3 runs
```

总计约 `30` 个 `TabICL` runs。

这比主线小，但仍然不是零成本。
所以后续脚本实现时仍应先 smoke test，再跑完整实验。

## 11. 下一阶段怎么接

下一步可以进入 Phase 6 实验脚本实现。

建议顺序是：

1. 新增 `src/phase6_big_plus_adult.py`
2. 复用 Phase 4/5 中的 Adult 数据加载、split、指标和 runtime 记录
3. 先实现四种支持集策略和配额函数
4. 先跑最小 smoke test：

```bash
python3 src/phase6_big_plus_adult.py --strategies random_subset balanced_random_subset balanced_prototype_retrieval --budgets 512 --seeds 42
```

5. smoke test 通过后，再运行完整 Adult 主实验：

```bash
python3 src/phase6_big_plus_adult.py --strategies full_context random_subset balanced_random_subset balanced_prototype_retrieval --budgets 512 2048 8192 --seeds 42 43 44
```

这一阶段最重要的是守住冻结方法。
如果结果不好，先记录和解释，不立即改算法。

## 12. 第二步：脚本实现与 smoke test（历史记录）

本节保留早期 smoke test 的工程记录。
完整 Adult 主实验和正式分析见第 13 节。

### 12.1 新增脚本

本步骤新增：

- `src/phase6_big_plus_adult.py`

这个脚本只做一件事：

> 在 `Adult` 上，用 `TabICL` 比较四种支持集选择策略。

它不新增模型，不调参，不运行 `Bank Marketing`，也不回头重跑 Phase 4/5 主线。

### 12.2 已实现的策略

脚本已实现四种策略：

- `full_context`
- `random_subset`
- `balanced_random_subset`
- `balanced_prototype_retrieval`

脚本默认是 smoke-test 友好的设置：

- strategies：默认 all four
- budgets：默认 `512`
- seeds：默认 `42`

完整 Adult 主实验需要显式传入：

```bash
python3 src/phase6_big_plus_adult.py \
  --strategies full_context random_subset balanced_random_subset balanced_prototype_retrieval \
  --budgets 512 2048 8192 \
  --seeds 42 43 44
```

### 12.3 Smoke test 命令

本次只运行：

```bash
python3 src/phase6_big_plus_adult.py --budgets 512 --seeds 42
```

它覆盖：

- 数据集：`Adult`
- 模型：`TabICL`
- seed：`42`
- budget：`512`
- 策略：四种策略全部运行

### 12.4 Smoke test 输出

生成文件：

- `results/phase6_big_plus_adult.csv`
- `results/phase6_big_plus_adult_summary.csv`

detail CSV 当前为 `4` 行：

```text
1 seed × (1 Full Context + 3 budget-limited strategies × 1 budget) = 4 rows
```

summary CSV 当前也为 `4` 行。

### 12.5 Smoke test 结果

这张表只用于检查脚本是否能跑通，不作为正式 Big Plus 结论。

| strategy | budget | requested_budget | actual_support_size | support_class_counts | accuracy | balanced_accuracy | macro_f1 | total_seconds |
| --- | --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| full_context | full | 39073 | 39073 | `{"<=50K": 29724, ">50K": 9349}` | 0.8729 | 0.7946 | 0.8135 | 235.5895 |
| random_subset | 512 | 512 | 512 | `{"<=50K": 410, ">50K": 102}` | 0.8402 | 0.7068 | 0.7381 | 13.5195 |
| balanced_random_subset | 512 | 512 | 512 | `{"<=50K": 256, ">50K": 256}` | 0.7870 | 0.8159 | 0.7532 | 36.6981 |
| balanced_prototype_retrieval | 512 | 512 | 512 | `{"<=50K": 256, ">50K": 256}` | 0.6967 | 0.7052 | 0.6540 | 8.4308 |

### 12.6 Schema 检查

detail CSV 包含这些列：

```text
dataset, seed, split, strategy, strategy_display, budget, requested_budget,
actual_support_size, support_class_counts, model, metric, accuracy,
balanced_accuracy, macro_f1, fit_seconds, predict_seconds, total_seconds,
device, full_train_size, test_size, n_samples_total, n_features_raw,
n_numeric_features, n_categorical_features, n_features_after_preprocessing,
retrieval_n_features_after_encoding, random_state, test_size_ratio,
data_cache, input_representation, selection_method, notes
```

summary CSV 包含这些列：

```text
dataset, strategy, strategy_display, budget, model, n_runs, seeds,
requested_budget_min, requested_budget_max, actual_support_size_min,
actual_support_size_max, support_class_counts, accuracy_mean, accuracy_std,
accuracy_min, accuracy_max, balanced_accuracy_mean, balanced_accuracy_std,
balanced_accuracy_min, balanced_accuracy_max, macro_f1_mean, macro_f1_std,
macro_f1_min, macro_f1_max, fit_seconds_median, predict_seconds_median,
total_seconds_median
```

已确认：

- `requested_budget` 无缺失
- `actual_support_size` 无缺失
- `support_class_counts` 无缺失
- 四种策略都已出现
- 当前只包含 `seed=42`
- 当前 budget 只包含 `512` 和 `full`

### 12.7 当前观察

这次 smoke test 已经暴露出一个重要工程事实：

- `Full Context` 的预测时间明显长于预算受限策略
- 后续完整 Adult 主实验虽然只有约 `30` 个 `TabICL` runs，但仍需要显式确认后再启动

方法层面暂时不能下正式结论。
尤其不能因为这次单 seed smoke test 中 `Balanced Prototype Retrieval` 指标较低，就立刻修改冻结方法。

### 12.8 下一步

下一步可以有两个选择：

1. 先做脚本审查和小修：
   - 检查 quota 分配函数
   - 检查 BPR 是否严格只使用训练 split
   - 检查输出列是否满足报告需要
2. 确认后再启动完整 Adult 主实验：
   - budgets：`512`, `2048`, `8192`
   - seeds：`42`, `43`, `44`
   - strategies：四种策略

这条提醒已经完成其历史作用。
完整 Adult 主实验完成后，正式结论见下一节。

## 13. Adult 主实验结果分析

### 13.1 复核结果

本次只读取已有结果文件，不重新运行实验：

- detail：`results/phase6_big_plus_adult.csv`
- summary：`results/phase6_big_plus_adult_summary.csv`

复核结论：

- detail 为 `30` 行，符合 `3 seeds × (1 full_context + 3 strategies × 3 budgets)`。
- summary 为 `10` 行，符合 `1 full_context + 3 strategies × 3 budgets`。
- detail 和 summary 都包含 `requested_budget`、`actual_support_size`、`support_class_counts`。
- `random_subset`、`balanced_random_subset`、`balanced_prototype_retrieval` 在同一个 `budget/seed` 下 `requested_budget` 一致。
- budget-limited 策略的 `actual_support_size` 都等于对应 budget。
- `full_context` 的 `actual_support_size` 为 `39073`。

### 13.2 生成的分析图

新增脚本：

- `src/phase6_make_big_plus_figures.py`

生成图表：

- `results/figures/phase6_big_plus_adult_accuracy.png`
- `results/figures/phase6_big_plus_adult_accuracy.pdf`
- `results/figures/phase6_big_plus_adult_balanced_accuracy.png`
- `results/figures/phase6_big_plus_adult_balanced_accuracy.pdf`
- `results/figures/phase6_big_plus_adult_macro_f1.png`
- `results/figures/phase6_big_plus_adult_macro_f1.pdf`
- `results/figures/phase6_big_plus_adult_total_seconds_median.png`
- `results/figures/phase6_big_plus_adult_total_seconds_median.pdf`
- `results/figures/phase6_big_plus_adult_bpr_delta.png`
- `results/figures/phase6_big_plus_adult_bpr_delta.pdf`

前三张图展示三种 budget-limited 策略随 budget 的性能变化，并把 `Full Context` 作为水平参考线。
runtime 图使用 log scale，突出 `Full Context` 与 budget-limited 策略的耗时差异。
BPR delta 图直接展示 `Balanced Prototype Retrieval` 相对 `Random Subset` 和 `Balanced Random Subset` 的均值差值。

### 13.3 汇总结果

| strategy | budget | n_runs | requested_budget | actual_support_size | accuracy_mean | balanced_accuracy_mean | macro_f1_mean | total_seconds_median |
| --- | --- | ---: | ---: | ---: | ---: | ---: | ---: | ---: |
| full_context | full | 3 | 39073 | 39073 | 0.8722 | 0.7919 | 0.8117 | 45.8005 |
| random_subset | 512 | 3 | 512 | 512 | 0.8438 | 0.7358 | 0.7592 | 3.4771 |
| random_subset | 2048 | 3 | 2048 | 2048 | 0.8573 | 0.7668 | 0.7873 | 2.5291 |
| random_subset | 8192 | 3 | 8192 | 8192 | 0.8654 | 0.7874 | 0.8038 | 4.6601 |
| balanced_random_subset | 512 | 3 | 512 | 512 | 0.7964 | 0.8180 | 0.7610 | 3.4701 |
| balanced_random_subset | 2048 | 3 | 2048 | 2048 | 0.8155 | 0.8295 | 0.7792 | 2.5361 |
| balanced_random_subset | 8192 | 3 | 8192 | 8192 | 0.8344 | 0.8293 | 0.7941 | 4.6720 |
| balanced_prototype_retrieval | 512 | 3 | 512 | 512 | 0.7020 | 0.7093 | 0.6588 | 3.2666 |
| balanced_prototype_retrieval | 2048 | 3 | 2048 | 2048 | 0.7336 | 0.7684 | 0.7002 | 2.4829 |
| balanced_prototype_retrieval | 8192 | 3 | 8192 | 8192 | 0.6437 | 0.7256 | 0.6253 | 4.7904 |

### 13.4 BPR 对比结论

`Balanced Prototype Retrieval` 没有优于 `Random Subset` / `Balanced Random Subset`。

| budget | metric | BPR - Random | BPR - Balanced Random |
| --- | --- | ---: | ---: |
| 512 | accuracy | -0.1418 | -0.0944 |
| 512 | balanced_accuracy | -0.0265 | -0.1086 |
| 512 | macro_f1 | -0.1004 | -0.1022 |
| 2048 | accuracy | -0.1237 | -0.0818 |
| 2048 | balanced_accuracy | 0.0016 | -0.0610 |
| 2048 | macro_f1 | -0.0871 | -0.0789 |
| 8192 | accuracy | -0.2217 | -0.1907 |
| 8192 | balanced_accuracy | -0.0618 | -0.1036 |
| 8192 | macro_f1 | -0.1784 | -0.1688 |

最重要的是：

- `BPR` 对 `Random Subset` 只有一个很小的 balanced accuracy 正 delta：`budget=2048` 时 `+0.0016`。
- `BPR` 对 `Balanced Random Subset` 在所有指标、所有预算下都是负 delta。
- 因此当前冻结版本的 Big Plus 不能写成“检索方法带来性能提升”。

### 13.5 runtime 结论

runtime 符合预期。
`Full Context` 的 median total runtime 为 `45.8005s`，显著高于预算受限策略。

budget-limited 策略的 median total runtime：

- `512`：约 `3.27s` 到 `3.48s`
- `2048`：约 `2.48s` 到 `2.54s`
- `8192`：约 `4.66s` 到 `4.79s`

这说明压缩支持集确实带来明显工程效率收益。
但是在当前冻结的 BPR 定义下，效率收益没有同时转化为性能收益。

### 13.6 后续论文/报告写法建议

建议把 Phase 6 写成一个诚实的 ablation：

> 在 Adult 上，简单的支持集压缩可以显著降低 `TabICL` 推理耗时；随机子集在 accuracy 和 macro-F1 上接近 full-context，类别平衡随机子集在 balanced accuracy 上更强。但当前冻结的 balanced prototype retrieval 没有超过随机 baseline，说明“靠近类别中心的原型样本”并不一定是 `TabICL` 最有效的上下文样本。

报告中应该强调：

- 这是一个有价值的负结果，不应该为了追分修改冻结方法。
- `Balanced Random Subset` 是比 `BPR` 更强的 budget-fair baseline。
- 如果后续继续探索检索方法，应明确进入新的 phase 或新的方法版本，而不是回改 Phase 6 冻结定义。

当前可以进入 Phase 6 结果整理和论文图表撰写。
不建议直接进入 Phase 7，也不建议在没有新假设的情况下追加长实验。
