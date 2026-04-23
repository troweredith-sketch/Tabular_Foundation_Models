# Phase 4：主线模型与数据集补齐（最终版）

这篇文档是 Phase 4 的最终学习型复盘。  
这一阶段的重点不是“再多跑几个模型”，而是把课程项目最核心的主线结果真正补齐：

- `4` 个模型
- `2` 个数据集
- `2` 条场景口径
- `5` 个 seeds
- `1` 套统一字段和记录方式

如果以后你忘了为什么 Phase 4 很关键，先回来读这篇。

## 阶段目标

Phase 4 的目标是把主线结果真正补完整，而不是继续停留在 `Adult + 2 models`。

这一阶段最后要解决 4 个问题：

1. `TabICL` 能不能正式接进当前项目主线
2. `XGBoost` 能不能和现有结果表保持同一口径
3. `Bank Marketing` 能不能在同一框架里无缝复用
4. 最终能不能形成“两个数据集、四个模型”的正式比较框架

## 这一阶段做了什么

这一阶段最后完成了 5 类工作：`模型接入`、`脚本统一`、`正式实验`、`结果汇总` 和 `文档收尾`。

### 1. 正式接入了 `TabICL`

我们先没有急着写脚本，而是先做了两步基础工作：

- 在项目本地 `.venv` 中安装 `tabicl==2.1.0`
- 直接读取包内源码，确认：
  - `TabICLClassifier` 的 sklearn 风格接口
  - 官方 checkpoint 版本
  - 内部 `TransformToNumerical` 的真实预处理方式

这样做的原因很简单：

> 如果连真实 API 和内部预处理都没搞清楚，后面写出来的统一比较脚本很容易是“看起来统一，实际上口径不一致”。

### 2. 写了统一的 Phase 4 主线脚本

这一阶段新增了：

- `src/phase4_mainline_compare.py`

这个脚本把主线统一成：

- 数据集：`Adult`、`Bank Marketing`
- 模型：`LightGBM`、`XGBoost`、`TabPFN v2`、`TabICL`
- 场景：`control_10k`、`full_train_reference`
- seeds：默认 `42 43 44 45 46`

它延续了 Phase 3 已经统一好的字段，包括：

- `dataset`
- `scenario`
- `seed`
- `split`
- `model`
- `accuracy`
- `fit_seconds`
- `predict_seconds`
- `total_seconds`
- `device`
- `train_size`
- `test_size`
- `n_samples_total`
- `n_features_raw`
- `n_numeric_features`
- `n_categorical_features`
- `n_features_after_preprocessing`
- `random_state`
- `test_size_ratio`
- `data_cache`
- `input_representation`
- `notes`

### 3. 保留了双场景主线

这一阶段我们没有把 Phase 3 的公平性思路丢掉，而是继续保留两条线：

#### `control_10k`

- 这是公平主证据
- 四个模型都使用同一个 seed 下的固定测试集
- 再从训练集里抽 `10,000` 条样本进行比较

#### `full_train_reference`

- 这是工程参考线
- 用完整训练集看真实 full-train 情况
- 其中 `TabPFN v2` 继续明确标注为带限制说明的受限条件结果

这一步非常重要，因为它让我们不需要在“公平比较”和“真实工程参考”之间二选一。

### 4. 完成了正式多 seed 运行

这一阶段最终真实跑完了：

- `2 datasets × 2 scenarios × 5 seeds × 4 models`

并生成：

- `results/phase4_mainline_compare.csv`
- `results/phase4_mainline_compare_summary.csv`

这样一来，Phase 4 不再是“先写脚本，结果以后再补”，而是真正有正式主表了。

### 5. 把结果和结论写回文档

这一阶段不是只留下脚本和结果文件。

我们还同步更新了：

- `docs/project_record.md`
- `docs/work_log.md`
- `docs/session_handoff.md`
- `docs/experiment_log.md`
- `docs/phase_plan.md`
- `README.md`

并新增当前阶段学习型文档：

- `notebooks/phase4_mainline_completion.md`

## 关键概念学习

### 1. “统一比较框架”不是把所有模型放进一张表就够了

真正的统一比较框架至少要做到：

- 同一套结果字段
- 同一套 split 逻辑
- 同一套场景命名
- 同一套汇总方式
- 同一套文档口径

如果只有结果放在一张表里，但字段、切分或备注都不统一，那只是“拼表”，不是统一框架。

### 2. 为什么 Phase 4 还要保留 `control_10k`

因为 Phase 3 已经证明了一件事：

> 如果不把更公平的支持范围场景单独保留下来，后面很容易把 full-train 参考线误当成正式主证据。

所以 Phase 4 虽然模型更多、数据集更多，但主证据依然优先看：

- `control_10k`

而不是直接把所有注意力都放到 full-train。

### 3. 为什么 `TabICL` 值得重点关注

这一阶段最有意思的新信息不是“又多了一个模型”，而是：

- `TabICL` 在 `Adult` 上已经接近树模型
- `TabICL` 在 `Bank Marketing` 上已经达到最强或并列最强
- `TabICL` 在两个数据集上都明显快于 `TabPFN v2`

这意味着它非常适合作为 Big Plus 的主方法入口。

### 4. 为什么要同时看准确率和运行时间

如果只看准确率，你会说：

- `Adult` 上树模型最强
- `Bank Marketing` 上 foundation model 很有潜力

但如果把运行时间一起看，你就会发现：

- 树模型仍然是最便宜的强基线
- `TabPFN v2` 的推理成本很高
- `TabICL` 处在一个很有意思的位置：
  - 比树模型慢
  - 但明显快于 `TabPFN v2`
  - 在部分数据集上准确率已经很有竞争力

## 为什么这样设计

这一阶段最后采用“`control_10k` + `full_train_reference`”双场景、统一脚本、多 seed 的设计，不是为了让实验看起来更复杂，而是为了同时回答不同问题。

### `control_10k` 回答的是

在更公平、更可比的支持范围里，四个模型的主线排序是什么？

这条线最适合写进正式结论，因为它更公平。

### `full_train_reference` 回答的是

如果直接用完整训练集，真实工程上会发生什么？

这条线的价值在于：

- 保留真实 full-train 参考
- 暴露 `TabPFN v2` 的限制
- 帮助后面在报告里解释“公平证据”和“工程参考”为什么不完全一样

### 两个数据集一起看回答的是

模型排序是不是只在一个数据集上成立？

如果只看 `Adult`，你可能会得出：

- foundation model 不如树模型

但把 `Bank Marketing` 放进来之后，你会发现：

- 这个结论并不是全局成立的
- 数据集不同，模型排序会改变

这正是双数据集主线的价值。

## 当前结果说明了什么

### 1. `Adult control_10k`

- `XGBoost = 0.8698 ± 0.0022`
- `LightGBM = 0.8692 ± 0.0014`
- `TabICL = 0.8681 ± 0.0026`
- `TabPFN v2 = 0.8614 ± 0.0031`

这说明：

- 树模型仍然是 `Adult` 上更稳的主线 baseline
- `XGBoost` 和 `LightGBM` 几乎并列
- `TabICL` 已经接近树模型，但还没有超越
- `TabPFN v2` 继续落后

### 2. `Adult full_train_reference`

- `LightGBM = 0.8752 ± 0.0025`
- `XGBoost = 0.8743 ± 0.0033`
- `TabICL = 0.8707 ± 0.0021`
- `TabPFN v2 = 0.8633 ± 0.0023`

这说明：

- full-train 参考线没有推翻 `Adult` 上树模型领先的方向
- `TabICL` 仍然优于 `TabPFN v2`
- `TabPFN v2` 依然需要带着限制说明来解释

### 3. `Bank Marketing control_10k`

- `TabICL = 0.9093 ± 0.0021`
- `TabPFN v2 = 0.9093 ± 0.0013`
- `LightGBM = 0.9044 ± 0.0014`
- `XGBoost = 0.9040 ± 0.0016`

这说明：

- foundation model 在 `Bank Marketing` 上开始展现优势
- `TabICL` 和 `TabPFN v2` 整体高于树模型
- `TabICL` 已经在准确率上进入第一梯队

### 4. `Bank Marketing full_train_reference`

- `TabICL = 0.9119 ± 0.0019`
- `TabPFN v2 = 0.9110 ± 0.0019`
- `LightGBM = 0.9083 ± 0.0015`
- `XGBoost = 0.9083 ± 0.0017`

这说明：

- `TabICL` 在 `Bank Marketing` 上已经达到最强
- `TabPFN v2` 也很强，但速度仍明显更慢
- 树模型在这里不再是最强准确率选手

### 5. 运行时间层面的结论

最重要的速度观察是：

- 树模型最快
- `TabICL` 明显快于 `TabPFN v2`

例如：

- `Adult full_train_reference`
  - `TabICL predict_seconds_median = 29.8600`
  - `TabPFN v2 predict_seconds_median = 79.8174`
- `Bank Marketing full_train_reference`
  - `TabICL predict_seconds_median = 21.7999`
  - `TabPFN v2 predict_seconds_median = 76.1499`

所以这一阶段最值得记住的一句话是：

> `TabICL` 不一定总是最准确，但它已经形成了一个“比树模型更像 foundation model、又比 TabPFN 更实用”的中间位置。

## 遇到的问题与风险

### 1. 仓库原本没有 `TabICL` 依赖

这意味着：

- 不能直接上手跑
- 必须先确认真实 API 和 checkpoint 逻辑

我们用“先装包，再读本地源码”的方式解决了这个问题。

### 2. `TabICL` 第一次运行需要 checkpoint

如果直接把第一次下载也算进计时，结果会失真。  
所以脚本里先做了 checkpoint 预热，再开始正式计时。

### 3. `TabPFN v2` 的 full-train 限制依然存在

这一点没有因为 Phase 4 就自动消失。

所以：

- `control_10k` 仍然是主证据
- `full_train_reference` 里的 `TabPFN v2` 仍然要带限制说明

### 4. Phase 5 不应该再回头改 Phase 4 主线

现在主线已经站稳了。  
最大的风险反而变成：

> 后面如果总想继续微调主线口径，就会拖慢 Big Plus。

所以从现在开始，Phase 4 主表应该视为固定参照，而不是继续重写的对象。

## 下一阶段怎么接

Phase 5 的重点不再是“把主线跑完整”，而是：

- 在 `Adult` 上正式提出 Big Plus 方法
- 围绕 `TabICL` 固定 4 种支持集策略
- 用上下文预算和多 seeds 做方法比较

当前最合适的推进顺序是：

1. 固定 `Full Context`、`Random Subset`、`Balanced Random Subset`、`Balanced Prototype Retrieval`
2. 在 `Adult` 上使用 `512 / 2048 / 8192` 三档上下文预算
3. 使用 `42 / 43 / 44` 三个 seeds
4. 先形成一轮 `Adult` 主深挖结果
5. 再决定何时进入 `Bank Marketing` 次验证

如果你只记一句话，请记这句：

> Phase 4 的意义，不只是把四个模型和两个数据集补齐，而是让项目第一次真正拥有了“可以直接写进报告主体”的统一主线结果表。
