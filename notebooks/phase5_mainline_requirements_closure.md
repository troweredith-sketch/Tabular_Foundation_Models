> Final source of truth: use report/report_draft.md, results/*.csv, and report/submission_manifest.md for the submitted results. This file may include historical planning or work-log context.

# Phase 5：主线硬要求闭环与结果补强

这篇文档是 Phase 5 的学习型 notebook。
当前先记录 Phase 5 的第一步：在 Phase 4 主线实验中补齐 `accuracy` 之外的分类指标。

这一步的关键词是：

- `balanced_accuracy`
- `macro_f1`
- 类别不平衡
- 主线结果可解释性
- 先 smoke test，不直接跑完整长实验

## 为什么 Phase 5 先补指标

Phase 4 已经完成了主线比较框架：

- 模型：`TabPFN v2`、`TabICL`、`LightGBM`、`XGBoost`
- 数据集：`Adult`、`Bank Marketing`
- 场景：`control_10k`、`full_train_reference`
- seeds：`42 43 44 45 46`

但 Phase 4 的一个明显不足是：

> 主结果只有 `accuracy`。

这对课程项目来说还不够稳，尤其是 `Bank Marketing` 这类类别不平衡数据集。
如果只看整体准确率，模型可能因为把多数类预测得很好而看起来分数不错，但对少数类的识别能力并不强。

所以 Phase 5 的第一步是：

> Phase 5 开始补齐 accuracy 之外的指标，以回应类别不平衡和原始要求中的模型优缺点分析。

这一步不改变 Big Plus 方向，不新增模型，也不扩展到 regression 或 survival analysis。

## 新增两个指标

### 1. `balanced_accuracy`

普通 `accuracy` 计算的是：

```text
预测正确的样本数 / 总样本数
```

如果数据集中多数类很多，模型只要偏向多数类，也可能得到不错的 `accuracy`。

`balanced_accuracy` 更关心每个类别是否都被照顾到。
它可以理解为：

```text
每个类别 recall 的平均值
```

所以它更适合用来补充分析类别不平衡问题。

### 2. `macro_f1`

`macro_f1` 会先分别计算每个类别的 F1-score，再对类别做简单平均。

它的特点是：

- 不按类别样本数加权
- 少数类和多数类在平均时权重相同
- 能帮助我们观察模型是否只对多数类表现好

因此，`macro_f1` 很适合和 `balanced_accuracy` 一起补充 `accuracy`。

## 本次代码改动位置

修改文件：

- `src/phase4_mainline_compare.py`

核心改动有 4 类。

### 1. 新增 sklearn 指标导入

原来只导入：

```python
from sklearn.metrics import accuracy_score
```

现在改为：

```python
from sklearn.metrics import accuracy_score, balanced_accuracy_score, f1_score
```

### 2. 新增统一指标计算函数

这次没有在四个模型函数里分别手写三遍指标，而是新增了一个 helper：

```python
def calculate_classification_metrics(y_true: object, y_pred: object) -> dict[str, object]:
    return {
        "metric": "accuracy",
        "accuracy": round(accuracy_score(y_true, y_pred), 4),
        "balanced_accuracy": round(balanced_accuracy_score(y_true, y_pred), 4),
        "macro_f1": round(f1_score(y_true, y_pred, average="macro", zero_division=0), 4),
    }
```

这样做的好处是：

- 四个模型的指标计算口径完全一致
- 后面如果再加指标，只需要改一个地方
- 不容易出现某个模型漏算某个指标的问题

这里 `zero_division=0` 的作用是：如果某个类别在预测里完全没有被预测出来，F1 的计算不会报错，而是把对应项设为 `0`。这对不平衡分类任务比较稳。

### 3. 四个模型结果都写入新指标

四个模型函数都从原来的：

```python
"metric": "accuracy",
"accuracy": round(accuracy_score(y_test, y_pred), 4),
```

改成类似：

```python
**calculate_classification_metrics(y_test, y_pred),
```

影响到的模型包括：

- `run_lightgbm`
- `run_xgboost`
- `run_tabpfn_v2`
- `run_tabicl`

其中 `XGBoost` 仍然使用 label-encoded 后的 `y_test_encoded` 和 `y_pred_encoded` 来计算指标，保持和原来 accuracy 的口径一致。

### 4. 扩展 detail 和 summary 的列

detail CSV 原来有：

```text
accuracy
```

现在新增：

```text
balanced_accuracy
macro_f1
```

summary CSV 原来聚合：

```text
accuracy_mean
accuracy_std
accuracy_min
accuracy_max
```

现在新增：

```text
balanced_accuracy_mean
balanced_accuracy_std
balanced_accuracy_min
balanced_accuracy_max
macro_f1_mean
macro_f1_std
macro_f1_min
macro_f1_max
```

原有字段仍然保留，包括：

- `accuracy`
- `fit_seconds`
- `predict_seconds`
- `total_seconds`
- `device`
- `train_size`
- `test_size`
- 其他实验记录字段

## 保持不变的实验范围

这次只补指标，不扩大实验范围。

保持不变的内容包括：

- 模型仍然是：
  - `TabPFN v2`
  - `TabICL`
  - `LightGBM`
  - `XGBoost`
- 数据集仍然是：
  - `Adult`
  - `Bank Marketing`
- 场景仍然是：
  - `control_10k`
  - `full_train_reference`
- 默认 seeds 仍然是：
  - `42 43 44 45 46`

这很重要，因为 Phase 5 当前任务是补齐主线硬要求，而不是把项目范围继续膨胀。

## Smoke Test

按要求先只跑最小测试：

```bash
python3 src/phase4_mainline_compare.py --datasets adult --scenarios control_10k --seeds 42
```

这次 smoke test 覆盖：

- `Adult`
- `control_10k`
- `seed = 42`
- 四个模型全部运行

运行成功后，终端打印中已经出现了新指标。

### Smoke test 结果

`Adult control_10k seed=42`：

| model | accuracy | balanced_accuracy | macro_f1 |
| --- | ---: | ---: | ---: |
| LightGBM | 0.8684 | 0.7924 | 0.8086 |
| XGBoost | 0.8681 | 0.7875 | 0.8062 |
| TabPFN v2 | 0.8621 | 0.7807 | 0.7981 |
| TabICL | 0.8703 | 0.7907 | 0.8095 |

这张表只用于确认代码和 CSV schema 正常，不应该当成完整 Phase 4 结论。

## CSV 审查

### Detail CSV

文件：

- `results/phase4_mainline_compare.csv`

表头现在包含：

```text
dataset,scenario,seed,split,model,metric,accuracy,balanced_accuracy,macro_f1,fit_seconds,predict_seconds,total_seconds,...
```

关键新增列：

- `balanced_accuracy`
- `macro_f1`

### Summary CSV

文件：

- `results/phase4_mainline_compare_summary.csv`

表头现在包含：

```text
accuracy_mean,accuracy_std,accuracy_min,accuracy_max,
balanced_accuracy_mean,balanced_accuracy_std,balanced_accuracy_min,balanced_accuracy_max,
macro_f1_mean,macro_f1_std,macro_f1_min,macro_f1_max,
fit_seconds_median,predict_seconds_median,total_seconds_median
```

关键新增列：

- `balanced_accuracy_mean`
- `balanced_accuracy_std`
- `balanced_accuracy_min`
- `balanced_accuracy_max`
- `macro_f1_mean`
- `macro_f1_std`
- `macro_f1_min`
- `macro_f1_max`

因为 smoke test 只跑了一个 seed，所以当前 summary 里的 std 是 `0.0`。
这不是问题，而是单 seed 聚合的正常结果。

## 这一步为什么不直接跑完整 Phase 4

完整 Phase 4 主线会跑：

```text
2 datasets × 2 scenarios × 5 seeds × 4 models
```

其中 `TabPFN v2` 和 `TabICL` 的运行时间明显更长。
所以这次遵循“先 smoke test，再确认是否完整重跑”的顺序。

当前状态是：

- 代码已经能计算新指标
- detail CSV 已经能写入新指标
- summary CSV 已经能聚合新指标
- smoke test 已通过
- 完整 Phase 4 主线重跑已在 2026-04-24 完成

## 当前需要注意的结果文件状态

运行 smoke test 会覆盖默认输出：

- `results/phase4_mainline_compare.csv`
- `results/phase4_mainline_compare_summary.csv`

为了避免原完整 Phase 4 结果丢失，本次先备份了原文件：

- `results/phase4_mainline_compare_pre_phase5_metrics_backup.csv`
- `results/phase4_mainline_compare_summary_pre_phase5_metrics_backup.csv`

后面如果确认重跑完整 Phase 4，新的正式结果会重新写回默认 CSV。

当前已经完成完整重跑，所以默认 CSV 已经是 Phase 5 指标补齐后的正式主线结果。

## 审查清单

后面审查这次改动时，可以按下面顺序看。

1. 看 `src/phase4_mainline_compare.py` 的 import：
   - 是否导入了 `balanced_accuracy_score`
   - 是否导入了 `f1_score`
2. 看 `calculate_classification_metrics`：
   - 是否同时返回 `accuracy`
   - 是否返回 `balanced_accuracy`
   - 是否返回 `macro_f1`
3. 看四个模型函数：
   - `LightGBM` 是否调用统一指标函数
   - `XGBoost` 是否调用统一指标函数
   - `TabPFN v2` 是否调用统一指标函数
   - `TabICL` 是否调用统一指标函数
4. 看 `DETAIL_COLUMN_ORDER`：
   - 是否包含 `balanced_accuracy`
   - 是否包含 `macro_f1`
5. 看 `SUMMARY_COLUMN_ORDER` 和 `build_summary`：
   - 是否聚合 `balanced_accuracy_mean/std/min/max`
   - 是否聚合 `macro_f1_mean/std/min/max`
6. 看 smoke test 输出：
   - detail CSV 是否有新列
   - summary CSV 是否有新列
   - 原有 accuracy 和运行时间列是否还在

## 完整重跑结果

smoke test 通过后，正式重跑了完整主线：

```bash
python3 src/phase4_mainline_compare.py \
  --datasets adult bank_marketing \
  --scenarios control_10k full_train_reference \
  --seeds 42 43 44 45 46
```

### 校验结果

- detail CSV：`80` 行
- summary CSV：`16` 行
- 每个 `dataset + scenario + model` 组合都有 `5` 个 seeds
- summary 中所有行的 `n_runs = 5`
- summary 中所有行的 `seeds = 42,43,44,45,46`
- detail 和 summary 都包含新增指标列

### 主线 summary

| dataset | scenario | model | accuracy_mean | balanced_accuracy_mean | macro_f1_mean |
| --- | --- | --- | ---: | ---: | ---: |
| adult | control_10k | LightGBM | 0.8692 | 0.7934 | 0.8097 |
| adult | control_10k | TabICL | 0.8681 | 0.7909 | 0.8077 |
| adult | control_10k | TabPFN v2 | 0.8614 | 0.7789 | 0.7966 |
| adult | control_10k | XGBoost | 0.8698 | 0.7887 | 0.8082 |
| adult | full_train_reference | LightGBM | 0.8752 | 0.8013 | 0.8183 |
| adult | full_train_reference | TabICL | 0.8707 | 0.7991 | 0.8133 |
| adult | full_train_reference | TabPFN v2 | 0.8633 | 0.7778 | 0.7977 |
| adult | full_train_reference | XGBoost | 0.8743 | 0.7953 | 0.8150 |
| bank_marketing | control_10k | LightGBM | 0.9044 | 0.7092 | 0.7367 |
| bank_marketing | control_10k | TabICL | 0.9093 | 0.7397 | 0.7606 |
| bank_marketing | control_10k | TabPFN v2 | 0.9093 | 0.7215 | 0.7504 |
| bank_marketing | control_10k | XGBoost | 0.9040 | 0.7019 | 0.7315 |
| bank_marketing | full_train_reference | LightGBM | 0.9083 | 0.7273 | 0.7524 |
| bank_marketing | full_train_reference | TabICL | 0.9119 | 0.7599 | 0.7745 |
| bank_marketing | full_train_reference | TabPFN v2 | 0.9110 | 0.7209 | 0.7523 |
| bank_marketing | full_train_reference | XGBoost | 0.9083 | 0.7184 | 0.7472 |

## 学习解读

### 1. 新指标会改变细粒度排序

在 `Adult control_10k` 中：

- `accuracy_mean` 最高的是 `XGBoost`
- `balanced_accuracy_mean` 和 `macro_f1_mean` 最高的是 `LightGBM`

这说明只看 `accuracy` 时，结论会更偏向整体正确率；加入 `balanced_accuracy` 和 `macro_f1` 后，可以更细地观察各类别表现。

### 2. `Bank Marketing` 更能体现新增指标价值

`Bank Marketing` 是类别更不平衡的数据集。
在 `control_10k` 中：

- `TabICL` 和 `TabPFN v2` 的 `accuracy_mean` 都是 `0.9093`
- 但 `TabICL balanced_accuracy_mean = 0.7397`
- `TabPFN v2 balanced_accuracy_mean = 0.7215`
- `TabICL macro_f1_mean = 0.7606`
- `TabPFN v2 macro_f1_mean = 0.7504`

所以报告里不能只写“两个 foundation models accuracy 并列”，还可以进一步写：

> 在不平衡类别指标上，`TabICL` 比 `TabPFN v2` 更强。

### 3. `TabICL` 仍然是 Big Plus 的合理入口

完整重跑后，`TabICL` 在 `Bank Marketing` 上的优势更清楚：

- `control_10k` 中 `balanced_accuracy_mean` 和 `macro_f1_mean` 领先
- `full_train_reference` 中三类指标都领先
- 推理时间仍明显低于 `TabPFN v2`

这没有改变 Big Plus 方向，反而让之后围绕 `TabICL` 做支持集选择改进更有依据。

## 下一步建议

Phase 5 的指标补齐已经完成。下一步不进入 Big Plus，而是继续补主线硬要求中的 train-size scalability：

- `512`
- `2048`
- `8192`
- `10000`
- `full`

目标是生成 size vs metric / runtime 的结果表。
这一步完成后，主线才更完整地覆盖原始要求中的 scalability。

## 第二步：Train-size Scalability

指标补齐后，Phase 5 的第二步是补 train-size scalability。

这一步的目的不是新增模型，也不是调参，而是固定当前主线范围，观察训练样本数变化时：

- 模型指标如何变化
- 训练时间如何变化
- 推理时间如何变化
- foundation models 和树模型在不同训练规模下的优缺点是否不同

本步骤记录的核心目的句是：

> Phase 5 第二步补齐 train-size scalability，用固定模型、固定数据集、固定指标观察不同训练规模下的性能和运行时间变化。

### 实验范围保持不变

模型仍然是：

- `TabPFN v2`
- `TabICL`
- `LightGBM`
- `XGBoost`

数据集仍然是：

- `Adult`
- `Bank Marketing`

指标仍然是：

- `accuracy`
- `balanced_accuracy`
- `macro_f1`
- `fit_seconds`
- `predict_seconds`
- `total_seconds`

默认 seeds 仍然是：

- `42`
- `43`
- `44`
- `45`
- `46`

### Train-size grid

完整 scalability 计划使用：

- `512`
- `2048`
- `8192`
- `10000`
- `full`

其中 `full` 使用每个 seed 下 train/test split 后的完整训练集。

### 新增脚本

本步骤新增：

- `src/phase5_scalability_compare.py`

它尽量复用 `src/phase4_mainline_compare.py` 中已有的逻辑：

- 数据加载
- 特征类型识别
- 预处理
- 四个模型训练
- 指标计算
- TabICL checkpoint 预热

新增脚本只负责：

- 解析 train-size grid
- 按 train size 抽取分层训练子集
- 写入独立的 Phase 5 scalability 结果表

### 输出文件

本步骤不覆盖 Phase 4 主线结果，而是写入新文件：

- `results/phase5_scalability_compare.csv`
- `results/phase5_scalability_compare_summary.csv`

### Smoke test

先只运行：

```bash
python3 src/phase5_scalability_compare.py --datasets adult --train-sizes 512 --seeds 42
```

这个 smoke test 覆盖：

- `Adult`
- `train_size = 512`
- `seed = 42`
- 四个原有模型

### Smoke test 结果

| model | accuracy | balanced_accuracy | macro_f1 | predict_seconds |
| --- | ---: | ---: | ---: | ---: |
| LightGBM | 0.8337 | 0.7527 | 0.7624 | 0.1397 |
| XGBoost | 0.8454 | 0.7707 | 0.7801 | 0.0615 |
| TabPFN v2 | 0.8433 | 0.7613 | 0.7738 | 3.8933 |
| TabICL | 0.8414 | 0.7583 | 0.7709 | 2.9735 |

这张表只用于确认脚本和结果 schema 正常，不应该作为完整 scalability 结论。

### CSV 审查

detail CSV 已包含：

- `dataset`
- `train_size_label`
- `train_size`
- `seed`
- `split`
- `model`
- `accuracy`
- `balanced_accuracy`
- `macro_f1`
- `fit_seconds`
- `predict_seconds`
- `total_seconds`
- `device`

summary CSV 已包含：

- `dataset`
- `train_size_label`
- `model`
- `n_runs`
- `seeds`
- `accuracy_mean`
- `accuracy_std`
- `accuracy_min`
- `accuracy_max`
- `balanced_accuracy_mean`
- `balanced_accuracy_std`
- `balanced_accuracy_min`
- `balanced_accuracy_max`
- `macro_f1_mean`
- `macro_f1_std`
- `macro_f1_min`
- `macro_f1_max`
- `fit_seconds_median`
- `predict_seconds_median`
- `total_seconds_median`

### 当前状态

- `src/phase5_scalability_compare.py` 已新增
- smoke test 已通过
- 完整 scalability 实验已完成
- `results/phase5_scalability_compare.csv` 已覆盖并生成完整结果
- `results/phase5_scalability_compare_summary.csv` 已覆盖并生成完整 summary
- Phase 4 输出文件没有被本实验写入：
  - `results/phase4_mainline_compare.csv`
  - `results/phase4_mainline_compare_summary.csv`

## 完整 Scalability 实验

完整实验命令：

```bash
python3 src/phase5_scalability_compare.py \
  --datasets adult bank_marketing \
  --train-sizes 512 2048 8192 10000 full \
  --seeds 42 43 44 45 46
```

这一步保持实验范围不变：

- 模型仍然是 `TabPFN v2`、`TabICL`、`LightGBM`、`XGBoost`
- 数据集仍然是 `Adult`、`Bank Marketing`
- train-size grid 仍然是 `512`、`2048`、`8192`、`10000`、`full`
- seeds 仍然是 `42`、`43`、`44`、`45`、`46`
- 指标仍然是 `accuracy`、`balanced_accuracy`、`macro_f1`
- runtime 仍然记录 `fit_seconds`、`predict_seconds`、`total_seconds`
- 不新增模型、不调参、不进入 Big Plus、不扩展到 regression 或 survival analysis

### 完整实验校验

完整实验结束后，CSV 校验通过：

- detail CSV：`200` 行
  - `2 datasets × 5 train sizes × 5 seeds × 4 models = 200`
- summary CSV：`40` 行
  - `2 datasets × 5 train sizes × 4 models = 40`
- 每个 summary 组合：`n_runs = 5`
- summary seeds：`42,43,44,45,46`
- detail 组合最小/最大行数：`5 / 5`
- duplicate detail rows：`0`
- required detail columns：无缺失
- required summary columns：无缺失
- smoke 覆盖仍可在最终 detail 中确认：
  - `Adult`
  - `train_size_label = 512`
  - `seed = 42`
  - 四个模型共 `4` 行

### Adult 结果观察

从 `512` 到 `full`，`macro_f1_mean` 的变化是：

| model | macro_f1@512 | macro_f1@full | delta |
| --- | ---: | ---: | ---: |
| LightGBM | 0.7513 | 0.8183 | +0.0670 |
| XGBoost | 0.7605 | 0.8150 | +0.0545 |
| TabICL | 0.7671 | 0.8133 | +0.0462 |
| TabPFN v2 | 0.7662 | 0.7977 | +0.0315 |

从 `512` 到 `full`，`total_seconds_median` 的变化是：

| model | total_seconds@512 | total_seconds@full | delta |
| --- | ---: | ---: | ---: |
| LightGBM | 0.1629 | 0.8572 | +0.6943 |
| XGBoost | 0.1297 | 1.2079 | +1.0782 |
| TabICL | 3.2788 | 22.3303 | +19.0515 |
| TabPFN v2 | 2.7220 | 84.1770 | +81.4550 |

Adult 上可以看到：

- 树模型从 `512` 到 `full` 的指标提升最明显，尤其是 `LightGBM`
- `TabPFN v2` 的 `macro_f1` 提升最小，但 runtime 增长最大
- `TabICL` 的 full runtime 远低于 `TabPFN v2`，但仍明显慢于树模型

### Bank Marketing 结果观察

从 `512` 到 `full`，`macro_f1_mean` 的变化是：

| model | macro_f1@512 | macro_f1@full | delta |
| --- | ---: | ---: | ---: |
| LightGBM | 0.6618 | 0.7524 | +0.0906 |
| XGBoost | 0.6697 | 0.7472 | +0.0775 |
| TabICL | 0.6815 | 0.7745 | +0.0930 |
| TabPFN v2 | 0.6587 | 0.7523 | +0.0936 |

从 `512` 到 `full`，`total_seconds_median` 的变化是：

| model | total_seconds@512 | total_seconds@full | delta |
| --- | ---: | ---: | ---: |
| LightGBM | 0.1872 | 0.7195 | +0.5323 |
| XGBoost | 0.1399 | 0.8875 | +0.7476 |
| TabICL | 3.6889 | 20.1147 | +16.4258 |
| TabPFN v2 | 2.7932 | 80.3920 | +77.5988 |

Bank Marketing 上可以看到：

- 所有模型随 train size 增大在 `balanced_accuracy` 和 `macro_f1` 上都有明显提升
- `TabICL` 和 `TabPFN v2` 在指标上整体更强，尤其 `TabICL` 的 `macro_f1@full` 最高
- `TabICL` 的 full runtime 明显低于 `TabPFN v2`
- 树模型 runtime 仍然保持在亚秒到约 `1` 秒量级

### Runtime 解释口径

这组 runtime 应该写成 practical mixed-device timing：

- 树模型在 CPU 上运行
- foundation models 在 CUDA 上运行
- 因此可以比较“当前本地环境下实际运行成本”
- 但不要把它写成严格同设备公平速度比较

另外，`full` train size 下 `TabPFN v2` 超过 `10,000` 样本官方支持范围，脚本使用 `ignore_pretraining_limits=True`。
所以 full 行应该作为 constrained reference result，而不是最干净的官方支持范围内结论。

## Phase 5 第二步结论

Phase 5 完整 train-size scalability 实验已经通过。
主线现在不仅有 `accuracy`、`balanced_accuracy`、`macro_f1`，也有跨训练规模的性能和 runtime 表格。

这一步完成后，项目已经更完整地覆盖原始要求中的：

- classification performance
- inference speed / runtime
- scalability across dataset sizes
- model pros / cons analysis

## 下一步建议

下一步可以进入 Phase 5 的图表/报告骨架整理：

- 生成 size-vs-metric 图表
- 生成 size-vs-runtime 图表
- 建立英文报告主线结构
- 建立 PPT 主线结构

Big Plus 仍然顺延，不在主线图表和报告骨架整理前抢占优先级。

## 第三步：主线图表和报告/PPT 骨架整理

Phase 5 的第三步不是继续扩实验，而是把已经完成的主线结果整理成可以写报告、做展示的材料。

本步骤的目的句是：

> Phase 5 第三步把已完成的主线实验结果整理成可用于英文报告和 15 分钟展示的图表与结构化叙事。

这一步仍然保持边界不变：

- 不进入 Big Plus
- 不新增模型
- 不调参
- 不扩展到 regression 或 survival analysis
- Big Plus 仍然保持为 Phase 6 的 `TabICL` 支持集选择方向

### 图表脚本

新增脚本：

- `src/phase5_make_mainline_figures.py`

它只读取已有结果：

- `results/phase5_scalability_compare_summary.csv`

它不会重跑实验，也不会改写 Phase 4/5 的结果 CSV。

### 生成图表

图表统一输出到：

- `results/figures/`

本步骤生成了 4 组图，每组同时保存 PNG 和 PDF：

- `phase5_scalability_accuracy`
- `phase5_scalability_balanced_accuracy`
- `phase5_scalability_macro_f1`
- `phase5_scalability_total_seconds_median`

每张图都使用两个 subplot：

- `Adult`
- `Bank Marketing`

x 轴 train-size 顺序固定为：

- `512`
- `2048`
- `8192`
- `10000`
- `full`

runtime 图使用 log-scale y 轴。这样树模型的亚秒级运行时间和 foundation models 的几十秒运行时间都能在同一张图里看清楚。

### 报告骨架

新增英文报告骨架：

- `report/outline.md`

它包含：

- Title
- Abstract draft
- Introduction
- Related / Background
- Datasets
- Models
- Experimental Setup
- Main Results
- Scalability Analysis
- Runtime Analysis
- Discussion
- Limitations
- Future Work / Big Plus Preview
- Conclusion

这份 outline 不是最终长篇报告，而是后续写正文时的结构化提纲。

### PPT 骨架

新增 15 分钟英文展示骨架：

- `slides/outline.md`

当前设计为 11 页。每页都包含：

- slide title
- key message
- suggested figure/table
- speaker note bullets

这让后续做真正 PPT 时，不需要重新想叙事顺序。

### 主线观察

这一阶段把主线观察整理成下面几条：

- `Adult` 上树模型整体更强，`TabICL` 接近树模型，`TabPFN v2` 相对弱且慢。
- `Bank Marketing` 上 foundation models 表现更亮，尤其 `TabICL` 在 `balanced_accuracy` 和 `macro_f1` 上更有优势。
- train size 增大时，多数指标提升，`Bank Marketing` 上提升尤其明显。
- runtime 随 train size 增大而上升，foundation models 增幅明显；`TabICL` 明显快于 `TabPFN v2`。

### 必须保留的 caveats

报告和 PPT 里必须继续保留这些限制说明：

- runtime caveat：树模型在 CPU 上运行，foundation models 可能使用 CUDA，因此这是 practical mixed-device timing，不是严格同设备公平速度比较。
- split caveat：实验使用 repeated stratified splits；每个 seed 内模型共享同一 split，但跨 seeds 不是同一个固定测试集。
- baseline caveat：`LightGBM` 和 `XGBoost` 是 fixed strong baselines，不是 tuned SOTA baselines。
- full-reference caveat：`full` train size 是工程参考结果；其中 `TabPFN v2` 超过更干净的 10k 支持范围口径。

### Phase 5 当前结论

Phase 5 第三步完成后，主线已经可以独立支撑课程报告。

换句话说，即使 Big Plus 后面结果一般，当前项目也已经有完整的主线故事：

- 四模型比较
- 两个主线数据集
- 多 seed 结果
- `accuracy`、`balanced_accuracy`、`macro_f1`
- train-size scalability
- runtime analysis
- pros / cons
- 报告和 PPT 骨架

后续已进入 Phase 6，并完成 `TabICL` 支持集选择 Big Plus 方法冻结。
下一步是实现 Adult 主实验脚本，并先做 smoke test。
