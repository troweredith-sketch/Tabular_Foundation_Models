# 实验记录

这份文档专门记录实验本身，后面写报告时可以直接从这里提取结果和观察。

建议每次实验至少记录：

- 日期
- 实验目的
- 数据集
- 模型
- 数据划分方式
- 评价指标
- 结果
- 观察
- 后续动作

---

## 实验 001：教学实验 - 决策树过拟合演示

### 日期

2026-04-16

### 实验目的

通过一个小型真实分类数据集，理解 `train/test split`、`accuracy` 和 `overfitting`。

### 数据集

`scikit-learn` 自带的 `breast_cancer` 数据集

### 模型

- 深树：`DecisionTreeClassifier(random_state=42)`
- 浅树：`DecisionTreeClassifier(max_depth=3, random_state=42)`

### 数据划分

- `test_size=0.2`
- `random_state=42`
- `stratify=y`

### 评价指标

- 训练集准确率
- 测试集准确率

### 结果

- 深树：`train_acc = 1.0000`，`test_acc = 0.9123`
- 浅树：`train_acc = 0.9758`，`test_acc = 0.9386`

### 观察

- 深树在训练集上达到满分，但测试集没有最好
- 浅树虽然训练集准确率略低，但测试集反而更高
- 这说明更复杂的模型更容易过拟合

### 结论

不能只看训练集表现，模型比较时必须重点看测试集结果。

### 下一步

把这种记录方式迁移到正式项目实验中，对真实数据集和 baseline 模型做同样记录。

---

## 实验 002：Adult 数据集上的第一个正式 Baseline

### 日期

2026-04-16

### 阶段归属

- 该实验已在 2026-04-22 被正式确认为 Phase 2 的官方 baseline 结果

### 实验目的

完成第二阶段目标：在第一个真实表格分类数据集上跑通一条完整 baseline 链路。

### 数据集

`Adult`（OpenML）

### 数据集观察

- 样本数：`48842`
- 原始特征数：`14`
- 数值特征数：`6`
- 类别特征数：`8`
- 有缺失值的列：`workclass`、`occupation`、`native-country`
- 目标类别：`<=50K` 和 `>50K`

### 模型

- `LightGBM`

### 预处理方式

- 数值列：`SimpleImputer(strategy='median')`
- 类别列：`SimpleImputer(strategy='most_frequent') + OneHotEncoder(handle_unknown='ignore')`
- 训练方式：`Pipeline + ColumnTransformer`

### 数据划分

- `test_size=0.2`
- `random_state=42`
- `stratify=y`

### 评价指标

- `accuracy`
- `fit_seconds`

### 结果

- `accuracy = 0.8751`
- `fit_seconds = 0.5361`
- `n_features_after_encoding = 105`

### 观察

- `Adult` 非常适合作为第一个正式数据集，因为它同时包含类别特征和缺失值
- baseline 已经成功跑通，说明第二阶段的核心目标已达成
- 这个结果现在最重要的意义是“建立参照物”，而不是宣布最终结论

### 结论

我们已经拥有第一条正式实验链路，后续可以在相同数据集和相同测试集上接入 `TabPFN v2`、`TabICL` 做公平对比。

### 下一步

- 接入 `TabPFN v2`
- 在 Adult 数据集上保持测试集一致
- 做第一次 foundation model vs baseline 对比

---

## 实验 003：Adult 数据集上的全量训练正式对比（受限条件结果，seed=42 锚点）

### 日期

2026-04-23

### 阶段归属

- 这是 Phase 3 的 `full Adult` 受限条件结果
- 这是后续多 seed 稳定性评估中的 `seed=42` 历史锚点结果
- 它保留在正式记录中，但不是 Phase 3 最终主证据

### 实验目的

在与 Phase 2 一致的 Adult 数据集上，保留一条最容易复现的 `seed=42` 全量训练对比结果，并明确记录它的限制条件。

### 数据集

`Adult`（OpenML，本地缓存）

### 场景

- `scenario = full_adult_limit_override`
- `split = adult_fixed_test_seed42_full_train`

### 模型

- `LightGBM`
- `TabPFN v2`

### 预处理方式

- `LightGBM`
  - 数值列：`SimpleImputer(strategy='median')`
  - 类别列：`SimpleImputer(strategy='most_frequent') + OneHotEncoder(handle_unknown='ignore')`
- `TabPFN v2`
  - 数值列：`SimpleImputer(strategy='median')`
  - 类别列：`SimpleImputer(strategy='most_frequent') + OrdinalEncoder(...)`
  - 显式传入类别特征索引

### 数据划分

- `test_size=0.2`
- `random_state=42`
- `stratify=y`
- 训练集使用全部 `39,073` 条样本
- 测试集固定为 `9,769` 条样本

### 评价指标

- `accuracy`
- `fit_seconds`
- `predict_seconds`
- `total_seconds`

### 结果

- `LightGBM`
  - `accuracy = 0.8751`
  - `fit_seconds = 0.9928`
  - `predict_seconds = 0.1000`
  - `total_seconds = 1.0928`
- `TabPFN v2`
  - `accuracy = 0.8650`
  - `fit_seconds = 3.3147`
  - `predict_seconds = 156.9472`
  - `total_seconds = 160.2619`

### 观察

- 在这次全量 Adult 对比里，`LightGBM` 的准确率高于 `TabPFN v2`
- `TabPFN v2` 的预测耗时远高于 `LightGBM`
- `TabPFN v2` 在这次运行中显式使用了 `ignore_pretraining_limits=True`
- 训练集大小为 `39,073`，超过了该比较中 `TabPFN v2` 官方 `10,000` 样本支持范围
- 因此这组结果是“真实可运行结果”，也是“受限条件结果”

### 结论

这组 `seed=42` full Adult 锚点结果说明：在当前设置下，`LightGBM` 在准确率和运行效率上都优于 `TabPFN v2`。  
但它还不是 Phase 3 最稳的主结论，因为 `TabPFN v2` 的运行超出了官方支持范围。  
因此这组结果应放在报告的“受限条件结果”或“讨论”部分，而不是单独作为最终主证据。

### 产出文件

- `python3 src/phase3_adult_compare.py --scenario full_adult_limit_override --seeds 42`
- `results/phase3_adult_compare.csv`

### 下一步

- 补做 `10,000` 样本控制实验的 `seed=42` 锚点
- 再补 `5` 个 seeds 的稳定性评估，把结论升级成 `mean ± std`

---

## 实验 004：Adult 数据集上的 10k 控制实验（seed=42 锚点）

### 日期

2026-04-23

### 阶段归属

- 这是 Phase 3 的控制实验锚点结果
- 它与实验 003 一起构成 Phase 3 的 `seed=42` 证据入口

### 实验目的

在保留同一个 Adult 测试集的前提下，把训练样本控制在 `10,000` 条以内，记录一条最容易复现的 `seed=42` 控制实验结果，检查 `TabPFN v2` 在官方支持范围内的表现。

### 数据集

`Adult`（OpenML，本地缓存）

### 场景

- `scenario = adult_control_10k`
- `split = adult_fixed_test_seed42_train10000`

### 模型

- `LightGBM`
- `TabPFN v2`

### 预处理方式

- `LightGBM`
  - 数值列：`SimpleImputer(strategy='median')`
  - 类别列：`SimpleImputer(strategy='most_frequent') + OneHotEncoder(handle_unknown='ignore')`
- `TabPFN v2`
  - 数值列：`SimpleImputer(strategy='median')`
  - 类别列：`SimpleImputer(strategy='most_frequent') + OrdinalEncoder(...)`
  - 显式传入类别特征索引

### 数据划分

- 先固定全数据测试集：
  - `test_size=0.2`
  - `random_state=42`
  - `stratify=y`
- 再从原始训练集 `39,073` 条样本中分层抽取 `10,000` 条作为控制实验训练子集
- 控制实验测试集与实验 003 完全相同，仍为 `9,769` 条样本

### 评价指标

- `accuracy`
- `fit_seconds`
- `predict_seconds`
- `total_seconds`

### 结果

- `LightGBM`
  - `accuracy = 0.8684`
  - `fit_seconds = 0.3606`
  - `predict_seconds = 0.1259`
  - `total_seconds = 0.4865`
- `TabPFN v2`
  - `accuracy = 0.8621`
  - `fit_seconds = 1.0290`
  - `predict_seconds = 25.7915`
  - `total_seconds = 26.8205`

### 控制条件说明

- 本次 `TabPFN v2` 未使用 `ignore_pretraining_limits=True`
- `10,000` 条训练样本可以直接运行，没有触发 `9,500` fallback

### 观察

- 在更公平的支持范围内，`LightGBM` 仍然略高于 `TabPFN v2`
- `TabPFN v2` 与 `LightGBM` 的准确率差距在这次锚点 run 中为 `0.0063`
- `TabPFN v2` 的预测耗时相比 full Adult 大幅下降，但仍明显高于 `LightGBM`
- 这说明 full Adult 结果的方向没有被推翻，只是现在有了一组更稳的主证据入口

### 与实验 003 的关系

- 实验 003 回答的是：
  “在 full Adult 训练集上，真实可运行的对比结果是什么？”
- 实验 004 回答的是：
  “在更公平、更符合支持范围的设置下，这个方向在 `seed=42` 下还成立吗？”

### 结论

Phase 3 的 `seed=42` 单次口径应建立在实验 004 之上：  
即使在更公平的支持范围内，`LightGBM` 仍然是 Adult 上更强或更高效的基线；实验 003 的方向没有被推翻。  
但 Phase 3 的最终结论不应只停留在一次 run，还需要继续看多 seed 的稳定性。

### 产出文件

- `python3 src/phase3_adult_compare.py --scenario adult_control_10k --seeds 42`
- `results/phase3_adult_compare_10k.csv`

### 下一步

- 做 `seeds = 42, 43, 44, 45, 46` 的多 seed 稳定性评估
- 用 `mean ± std` 来完成 Phase 3 最终结论

---

## 实验 005：Phase 3 多 seed 稳定性评估

### 日期

2026-04-23

### 阶段归属

- 这是升级后的 Phase 3 最终主证据
- 它把实验 003 和实验 004 从“单次锚点结果”升级成“多 seed 汇总结论”

### 实验目的

把 Phase 3 从“一次固定设置结果”升级成“多 seed 稳定性结果”，检查：

- full Adult 受限条件结果的方向是否稳定
- `10k control` 主证据的方向是否稳定
- `LightGBM` 与 `TabPFN v2` 的差距在不同随机划分下波动有多大

### 数据集

`Adult`（OpenML，本地缓存）

### 场景

- `full_adult_limit_override`
- `adult_control_10k`

### 模型

- `LightGBM`
- `TabPFN v2`

### 实验设置

- 默认 seeds：`42, 43, 44, 45, 46`
- 对每个 seed：
  - 先用该 seed 做 `train/test split`
  - `full` 场景用完整训练集
  - `10k control` 场景再从训练集内部分层抽取 `10,000` 条
- `full` 场景中 `TabPFN v2` 使用 `ignore_pretraining_limits=True`
- `10k control` 场景中 `TabPFN v2` 不使用 `ignore_pretraining_limits=True`
- `10,000` 条设置在 5 个 seeds 下都可直接运行，没有触发 `9,500` fallback

### 评价指标

- `accuracy_mean ± accuracy_std`
- `accuracy_min`
- `accuracy_max`
- `fit_seconds_median`
- `predict_seconds_median`

### 汇总结果

#### 1. `adult_control_10k`

- `LightGBM`
  - `accuracy_mean = 0.8692`
  - `accuracy_std = 0.0014`
  - `accuracy_min = 0.8677`
  - `accuracy_max = 0.8712`
  - `fit_seconds_median = 0.3842`
  - `predict_seconds_median = 0.1217`
- `TabPFN v2`
  - `accuracy_mean = 0.8614`
  - `accuracy_std = 0.0031`
  - `accuracy_min = 0.8561`
  - `accuracy_max = 0.8641`
  - `fit_seconds_median = 0.4061`
  - `predict_seconds_median = 22.3014`

#### 2. `full_adult_limit_override`

- `LightGBM`
  - `accuracy_mean = 0.8752`
  - `accuracy_std = 0.0025`
  - `accuracy_min = 0.8721`
  - `accuracy_max = 0.8781`
  - `fit_seconds_median = 0.9925`
  - `predict_seconds_median = 0.0914`
- `TabPFN v2`
  - `accuracy_mean = 0.8633`
  - `accuracy_std = 0.0023`
  - `accuracy_min = 0.8597`
  - `accuracy_max = 0.8654`
  - `fit_seconds_median = 1.6503`
  - `predict_seconds_median = 171.7491`

### 观察

- 在 `10k control` 这个更公平的主证据场景里，`LightGBM` 的均值仍高于 `TabPFN v2`
- `10k control` 的均值差距约为 `0.0078`，方向与 seed42 锚点一致
- 在 `full Adult` 受限条件场景里，`LightGBM` 的均值也稳定高于 `TabPFN v2`
- `TabPFN v2` 在 `10k control` 下的预测耗时相比 `full Adult` 大幅下降，但仍显著慢于 `LightGBM`
- `TabPFN v2` 在 `10k control` 下的准确率波动略大于 `LightGBM`

### 结论

升级后的 Phase 3 最终口径应优先引用实验 005：  
先报告 `10k control` 的 `accuracy_mean ± std`，再把 `full Adult` 作为受限条件结果补充。  

因此，Phase 3 的最终写法应为：

> 在 `Adult` 分类任务、当前 `ModelVersion.V2` 和本项目的实验设置下，`LightGBM` 在 `10k control` 的多 seed 结果中仍是更稳的主线 baseline；`full Adult` 的方向没有被推翻，但它仍应作为带限制说明的受限条件结果来呈现。

### 产出文件

- `python3 src/phase3_adult_compare.py`
- `results/phase3_adult_compare.csv`
- `results/phase3_adult_compare_10k.csv`
- `results/phase3_adult_compare_summary.csv`

### 下一步

- 将 Phase 3 的最终口径改为优先引用实验 005
- 进入 Phase 4：接入 `TabICL`、补齐 `XGBoost`、扩展到 `Bank Marketing`

---

## 实验记录模板

### 日期

YYYY-MM-DD

### 实验目的

- 

### 数据集

- 

### 模型

- 

### 数据划分

- 

### 评价指标

- 

### 结果

- 

### 观察

- 

### 结论

- 

### 下一步

- 
