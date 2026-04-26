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

## 实验 006：Phase 4 四模型双数据集统一主线比较

### 日期

2026-04-23

### 阶段归属

- 这是 Phase 4 的正式主线实验
- 它将主线比较从 `Adult + 2 models` 扩展为 `2 datasets + 4 models`
- 这是后续 Big Plus 的正式主线参照表

### 实验目的

完成 Phase 4 的主目标：

- 在 `Adult` 上正式接入 `TabICL`
- 将 `XGBoost` 纳入统一主线比较
- 将主线扩展到 `Bank Marketing`
- 形成四模型、双数据集、统一字段、统一口径的正式结果表

### 数据集

- `Adult`（OpenML，本地缓存）
- `Bank Marketing`（OpenML，本地缓存）

### 场景

- `control_10k`
- `full_train_reference`

说明：

- `control_10k` 是公平主证据场景
- `full_train_reference` 是工程参考线
- 在 `full_train_reference` 中，`TabPFN v2` 仍然是带限制说明的受限条件结果

### 模型

- `LightGBM`
- `XGBoost`
- `TabPFN v2`
- `TabICL`

### 实验设置

- 默认 seeds：`42, 43, 44, 45, 46`
- 对每个 `dataset + seed`：
  - 先做 `test_size=0.2`、`stratify=y` 的固定测试集划分
  - `control_10k` 场景从训练集内部分层抽取 `10,000` 条样本
  - `full_train_reference` 场景使用完整训练集
- 预处理与输入方式：
  - `LightGBM` / `XGBoost`
    - 数值列：`SimpleImputer(strategy='median')`
    - 类别列：`SimpleImputer(strategy='most_frequent') + OneHotEncoder(handle_unknown='ignore')`
  - `TabPFN v2`
    - 数值列：`SimpleImputer(strategy='median')`
    - 类别列：`SimpleImputer(strategy='most_frequent') + OrdinalEncoder(...)`
  - `TabICL`
    - 使用 `TabICLClassifier`
    - 使用官方 checkpoint：`tabicl-classifier-v2-20260212.ckpt`
    - 使用内部 `TransformToNumerical`
- `TabPFN v2` 在 `full_train_reference` 中使用 `ignore_pretraining_limits=True`

### 评价指标

- `accuracy_mean ± accuracy_std`
- `accuracy_min`
- `accuracy_max`
- `fit_seconds_median`
- `predict_seconds_median`
- `total_seconds_median`

### 汇总结果

#### 1. `Adult`

##### `control_10k`

- `XGBoost`
  - `accuracy_mean = 0.8698`
  - `accuracy_std = 0.0022`
  - `predict_seconds_median = 0.0501`
- `LightGBM`
  - `accuracy_mean = 0.8692`
  - `accuracy_std = 0.0014`
  - `predict_seconds_median = 0.0995`
- `TabICL`
  - `accuracy_mean = 0.8681`
  - `accuracy_std = 0.0026`
  - `predict_seconds_median = 4.3102`
- `TabPFN v2`
  - `accuracy_mean = 0.8614`
  - `accuracy_std = 0.0031`
  - `predict_seconds_median = 11.6090`

##### `full_train_reference`

- `LightGBM`
  - `accuracy_mean = 0.8752`
  - `accuracy_std = 0.0025`
  - `predict_seconds_median = 0.1044`
- `XGBoost`
  - `accuracy_mean = 0.8743`
  - `accuracy_std = 0.0033`
  - `predict_seconds_median = 0.0583`
- `TabICL`
  - `accuracy_mean = 0.8707`
  - `accuracy_std = 0.0021`
  - `predict_seconds_median = 29.8600`
- `TabPFN v2`
  - `accuracy_mean = 0.8633`
  - `accuracy_std = 0.0023`
  - `predict_seconds_median = 79.8174`

#### 2. `Bank Marketing`

##### `control_10k`

- `TabICL`
  - `accuracy_mean = 0.9093`
  - `accuracy_std = 0.0021`
  - `predict_seconds_median = 4.7736`
- `TabPFN v2`
  - `accuracy_mean = 0.9093`
  - `accuracy_std = 0.0013`
  - `predict_seconds_median = 12.9787`
- `LightGBM`
  - `accuracy_mean = 0.9044`
  - `accuracy_std = 0.0014`
  - `predict_seconds_median = 0.0942`
- `XGBoost`
  - `accuracy_mean = 0.9040`
  - `accuracy_std = 0.0016`
  - `predict_seconds_median = 0.0557`

##### `full_train_reference`

- `TabICL`
  - `accuracy_mean = 0.9119`
  - `accuracy_std = 0.0019`
  - `predict_seconds_median = 21.7999`
- `TabPFN v2`
  - `accuracy_mean = 0.9110`
  - `accuracy_std = 0.0019`
  - `predict_seconds_median = 76.1499`
- `LightGBM`
  - `accuracy_mean = 0.9083`
  - `accuracy_std = 0.0015`
  - `predict_seconds_median = 0.0835`
- `XGBoost`
  - `accuracy_mean = 0.9083`
  - `accuracy_std = 0.0017`
  - `predict_seconds_median = 0.0474`

### 观察

- 在 `Adult control_10k` 这个更公平的主证据场景里，最强 baseline 仍是树模型，`XGBoost` 仅以非常小的优势高于 `LightGBM`
- `TabICL` 在 `Adult` 上已经接近树模型，但还没有超越 `XGBoost / LightGBM`
- 在 `Bank Marketing` 上，foundation model 开始表现出优势：`TabICL` 和 `TabPFN v2` 的准确率整体高于树模型
- `TabICL` 在 `Bank Marketing` 上与 `TabPFN v2` 准确率相近，但预测速度明显更快
- 在两个数据集上，`TabPFN v2` 都是最慢的模型；`TabICL` 则形成了“比树模型慢、但明显快于 TabPFN v2”的中间位置

### 结论

Phase 4 已经完成主线补齐，当前项目的正式主线口径可以写成：

> 在当前统一比较框架下，树模型在 `Adult` 上仍然是更稳的主线 baseline；而在 `Bank Marketing` 上，foundation model 尤其是 `TabICL` 已经展现出更强的准确率潜力。与此同时，`TabICL` 相对 `TabPFN v2` 具有更好的运行效率，因此它适合作为后续 Big Plus 的主方法入口。

### 产出文件

- `python3 src/phase4_mainline_compare.py --datasets adult bank_marketing --scenarios control_10k full_train_reference --seeds 42 43 44 45 46`
- `src/phase4_mainline_compare.py`
- `results/phase4_mainline_compare.csv`
- `results/phase4_mainline_compare_summary.csv`

### 下一步

- 正式进入 Phase 5
- 在 `Adult` 上围绕 `TabICL` 设计并比较 4 种支持集策略
- 先形成 Big Plus 的主数据集证据，再决定何时进入 `Bank Marketing` 次验证

---

## 实验 007：Phase 5 主线指标补齐 smoke test

### 日期

2026-04-24

### 阶段归属

- 这是 Phase 5 的第一步：补齐主线实验指标
- 不改变 Big Plus 方向
- 不新增模型
- 不扩展到 regression 或 survival analysis

### 实验目的

Phase 5 开始补齐 accuracy 之外的指标，以回应类别不平衡和原始要求中的模型优缺点分析。

本次只先修改主线脚本并做 smoke test，确认新增指标能正确进入 detail CSV 和 summary CSV；不直接启动完整 Phase 4 主线重跑。

### 数据集

- `Adult`（OpenML，本地缓存）

### 场景

- `control_10k`

### 模型

- `LightGBM`
- `XGBoost`
- `TabPFN v2`
- `TabICL`

### 实验设置

- seed：`42`
- 命令：
  - `python3 src/phase4_mainline_compare.py --datasets adult --scenarios control_10k --seeds 42`

### 评价指标

- `accuracy`
- `balanced_accuracy`
- `macro_f1`
- `fit_seconds`
- `predict_seconds`
- `total_seconds`

### 结果

- smoke test 成功完成
- `results/phase4_mainline_compare.csv` 已包含：
  - `balanced_accuracy`
  - `macro_f1`
- `results/phase4_mainline_compare_summary.csv` 已包含：
  - `balanced_accuracy_mean`
  - `balanced_accuracy_std`
  - `balanced_accuracy_min`
  - `balanced_accuracy_max`
  - `macro_f1_mean`
  - `macro_f1_std`
  - `macro_f1_min`
  - `macro_f1_max`

### 观察

- `Adult control_10k seed=42` 下四个模型都能正常写出新增指标
- summary 中单 seed 的新增指标标准差为 `0.0`，符合当前 smoke test 只有一个 seed 的设置
- 原有 `accuracy` 和运行时间字段仍保留

### 下一步

- 等确认后再重跑完整 Phase 4 主线：
  - `Adult`、`Bank Marketing`
  - `control_10k`、`full_train_reference`
  - seeds `42 43 44 45 46`
  - 四个原有模型
- 完整重跑后再基于 `balanced_accuracy` 和 `macro_f1` 更新主线结果解释

---

## 实验 008：Phase 5 完整主线指标补齐重跑

### 日期

2026-04-24

### 阶段归属

- 这是 Phase 5 的指标闭环正式结果
- 不改变 Big Plus 方向
- 不新增模型
- 不扩展到 regression 或 survival analysis

### 实验目的

在实验 007 smoke test 成功后，完整重跑 Phase 4 主线实验，让所有主线结果都同时包含：

- `accuracy`
- `balanced_accuracy`
- `macro_f1`
- `fit_seconds`
- `predict_seconds`
- `total_seconds`

这样后续报告可以不只依赖 `accuracy`，也能更稳地讨论类别不平衡数据集上的模型优缺点。

### 数据集

- `Adult`（OpenML，本地缓存）
- `Bank Marketing`（OpenML，本地缓存）

### 场景

- `control_10k`
- `full_train_reference`

### 模型

- `LightGBM`
- `XGBoost`
- `TabPFN v2`
- `TabICL`

### 实验设置

- seeds：`42, 43, 44, 45, 46`
- 命令：
  - `python3 src/phase4_mainline_compare.py --datasets adult bank_marketing --scenarios control_10k full_train_reference --seeds 42 43 44 45 46`

### 评价指标

- detail CSV：
  - `accuracy`
  - `balanced_accuracy`
  - `macro_f1`
  - `fit_seconds`
  - `predict_seconds`
  - `total_seconds`
- summary CSV：
  - `accuracy_mean/std/min/max`
  - `balanced_accuracy_mean/std/min/max`
  - `macro_f1_mean/std/min/max`
  - `fit_seconds_median`
  - `predict_seconds_median`
  - `total_seconds_median`

### 校验结果

- `results/phase4_mainline_compare.csv`：`80` 行 detail 结果
- `results/phase4_mainline_compare_summary.csv`：`16` 行 summary 结果
- 每个 `dataset + scenario + model` 组合都有 `5` 个 seeds
- summary 中所有行的 `n_runs = 5`
- summary 中所有行的 `seeds = 42,43,44,45,46`
- 所有新增指标列均存在

### 汇总结果

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

### 观察

- `Adult control_10k` 中，`accuracy` 上 `XGBoost` 略高；但 `balanced_accuracy` 和 `macro_f1` 上 `LightGBM` 更高，说明新增指标确实会影响细粒度解读。
- `Bank Marketing control_10k` 中，`TabICL` 与 `TabPFN v2` 的 `accuracy_mean` 相同，但 `TabICL` 的 `balanced_accuracy_mean` 和 `macro_f1_mean` 明显更高，更适合用来说明类别不平衡下的优缺点。
- `Bank Marketing full_train_reference` 中，`TabICL` 在三类指标上都领先，并且仍明显快于 `TabPFN v2`。
- `balanced_accuracy` 和 `macro_f1` 让 `Bank Marketing` 的结论更清楚：不能只说 foundation models accuracy 更高，还可以指出 `TabICL` 对不平衡类别的综合表现更强。

### 结论

Phase 5 的第一块指标补齐已经完成。
当前主线结果已经覆盖 `accuracy`、`balanced_accuracy`、`macro_f1` 和运行时间，可以支撑后续报告中的模型优缺点分析。

### 产出文件

- `results/phase4_mainline_compare.csv`
- `results/phase4_mainline_compare_summary.csv`

### 下一步

- 进入 Phase 5 第二块：train-size scalability
- 默认 size grid 仍按阶段计划：
  - `512`
  - `2048`
  - `8192`
  - `10000`
  - `full`
- 优先生成 size vs metric / runtime 结果表，不新增模型、不调参、不进入 Big Plus

---

## 实验 009：Phase 5 train-size scalability smoke test

### 日期

2026-04-24

### 阶段归属

- 这是 Phase 5 第二步：train-size scalability 的 smoke test
- 不改变 Big Plus 方向
- 不新增模型
- 不调参
- 不扩展到 regression 或 survival analysis

### 实验目的

Phase 5 第二步补齐 train-size scalability，用固定模型、固定数据集、固定指标观察不同训练规模下的性能和运行时间变化。

本次只先新增 scalability 脚本并做最小 smoke test，确认脚本、CSV schema 和四模型输出都正常；不直接启动完整 scalability 长实验。

### 数据集

- `Adult`（OpenML，本地缓存）

### Train-size 设置

- `train_size_label = 512`
- `train_size = 512`

### 模型

- `LightGBM`
- `XGBoost`
- `TabPFN v2`
- `TabICL`

### 实验设置

- seed：`42`
- 命令：
  - `python3 src/phase5_scalability_compare.py --datasets adult --train-sizes 512 --seeds 42`

### 评价指标

- `accuracy`
- `balanced_accuracy`
- `macro_f1`
- `fit_seconds`
- `predict_seconds`
- `total_seconds`

### 结果

| model | accuracy | balanced_accuracy | macro_f1 | predict_seconds |
| --- | ---: | ---: | ---: | ---: |
| LightGBM | 0.8337 | 0.7527 | 0.7624 | 0.1397 |
| XGBoost | 0.8454 | 0.7707 | 0.7801 | 0.0615 |
| TabPFN v2 | 0.8433 | 0.7613 | 0.7738 | 3.8933 |
| TabICL | 0.8414 | 0.7583 | 0.7709 | 2.9735 |

### 校验结果

- `results/phase5_scalability_compare.csv` 已生成，包含 `4` 行 detail 结果
- `results/phase5_scalability_compare_summary.csv` 已生成，包含 `4` 行 summary 结果
- 四个模型都正常输出
- detail CSV 已包含：
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
- summary CSV 已包含：
  - `dataset`
  - `train_size_label`
  - `model`
  - `n_runs`
  - `seeds`
  - `accuracy_mean/std/min/max`
  - `balanced_accuracy_mean/std/min/max`
  - `macro_f1_mean/std/min/max`
  - `fit_seconds_median`
  - `predict_seconds_median`
  - `total_seconds_median`

### 观察

- `512` 训练样本下四个模型都能正常运行，说明新脚本可以复用 Phase 4 的数据加载、预处理、训练和指标逻辑。
- 在这个单 seed smoke test 中，`XGBoost` 的三类指标最高，但这只是 schema 和流程验证，不应当作为完整 scalability 结论。
- `TabICL` 在 `512` 样本下的预测时间仍短于 `TabPFN v2`，这个方向后续可在完整 scalability 结果中继续观察。

### 结论

Phase 5 train-size scalability 的 smoke test 通过。
后续完整 scalability 长实验已在实验 010 中完成。

### 产出文件

- `src/phase5_scalability_compare.py`
- `results/phase5_scalability_compare.csv`
- `results/phase5_scalability_compare_summary.csv`

### 下一步

- 进入实验 010 的完整 scalability 结果记录。
- 不新增模型、不调参、不进入 Big Plus。

---

## 实验 010：Phase 5 完整 train-size scalability 实验

### 日期

2026-04-24

### 阶段归属

- 这是 Phase 5 第二步的完整实验
- 不改变 Big Plus 方向
- 不新增模型
- 不调参
- 不扩展到 regression 或 survival analysis

### 实验目的

Phase 5 第二步补齐 train-size scalability，用固定模型、固定数据集、固定指标观察不同训练规模下的性能和运行时间变化。

### 数据集

- `Adult`（OpenML，本地缓存）
- `Bank Marketing`（OpenML，本地缓存）

### Train-size grid

- `512`
- `2048`
- `8192`
- `10000`
- `full`

其中 `full` 表示每个 seed 下 `train/test split` 后的完整训练集：

- `Adult full train_size = 39073`
- `Bank Marketing full train_size = 36168`

### 模型

- `LightGBM`
- `XGBoost`
- `TabPFN v2`
- `TabICL`

### 实验设置

- seeds：`42, 43, 44, 45, 46`
- split protocol：repeated stratified splits；每个 seed 内四个模型共享同一个 train/test split，跨 seeds 是不同的 stratified split
- 命令：

```bash
python3 src/phase5_scalability_compare.py \
  --datasets adult bank_marketing \
  --train-sizes 512 2048 8192 10000 full \
  --seeds 42 43 44 45 46
```

### 评价指标

- `accuracy`
- `balanced_accuracy`
- `macro_f1`
- `fit_seconds`
- `predict_seconds`
- `total_seconds`

### 输出文件

- 覆盖并生成：
  - `results/phase5_scalability_compare.csv`
  - `results/phase5_scalability_compare_summary.csv`
- 本实验没有写入 Phase 4 输出文件：
  - `results/phase4_mainline_compare.csv`
  - `results/phase4_mainline_compare_summary.csv`

### 完整性校验

- 实验退出码：`0`
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

### 主要结果：Adult

从 `512` 到 `full`，`macro_f1_mean` 变化如下：

| model | macro_f1@512 | macro_f1@full | delta |
| --- | ---: | ---: | ---: |
| LightGBM | 0.7513 | 0.8183 | +0.0670 |
| XGBoost | 0.7605 | 0.8150 | +0.0545 |
| TabICL | 0.7671 | 0.8133 | +0.0462 |
| TabPFN v2 | 0.7662 | 0.7977 | +0.0315 |

对应 `total_seconds_median` 变化如下：

| model | total_seconds@512 | total_seconds@full | delta |
| --- | ---: | ---: | ---: |
| LightGBM | 0.1629 | 0.8572 | +0.6943 |
| XGBoost | 0.1297 | 1.2079 | +1.0782 |
| TabICL | 3.2788 | 22.3303 | +19.0515 |
| TabPFN v2 | 2.7220 | 84.1770 | +81.4550 |

### 主要结果：Bank Marketing

从 `512` 到 `full`，`macro_f1_mean` 变化如下：

| model | macro_f1@512 | macro_f1@full | delta |
| --- | ---: | ---: | ---: |
| LightGBM | 0.6618 | 0.7524 | +0.0906 |
| XGBoost | 0.6697 | 0.7472 | +0.0775 |
| TabICL | 0.6815 | 0.7745 | +0.0930 |
| TabPFN v2 | 0.6587 | 0.7523 | +0.0936 |

对应 `total_seconds_median` 变化如下：

| model | total_seconds@512 | total_seconds@full | delta |
| --- | ---: | ---: | ---: |
| LightGBM | 0.1872 | 0.7195 | +0.5323 |
| XGBoost | 0.1399 | 0.8875 | +0.7476 |
| TabICL | 3.6889 | 20.1147 | +16.4258 |
| TabPFN v2 | 2.7932 | 80.3920 | +77.5988 |

### 观察

- `Adult` 上，树模型从 `512` 到 `full` 的 `macro_f1` 提升最大，尤其是 `LightGBM`；`TabPFN v2` 指标提升最小，但 runtime 增幅最大。
- `Bank Marketing` 上，所有模型随 train size 增大在 `balanced_accuracy` 和 `macro_f1` 上都有明显提升；`TabICL` 和 `TabPFN v2` 在指标上整体更强。
- `TabICL` 的 full runtime 明显低于 `TabPFN v2`：在两个数据集上约 `20-22` 秒量级，而 `TabPFN v2` 约 `80` 秒量级。
- runtime 变化最明显来自 foundation models；树模型在当前固定参数下仍保持亚秒到约 `1` 秒量级。

### Caveats

- runtime 是 practical mixed-device timing：树模型在 CPU，foundation models 在 CUDA；可以作为本地实际运行成本参考，但不应解释成严格同设备公平速度比较。
- `full` train size 下 `TabPFN v2` 超过 `10,000` 样本官方支持范围，脚本使用 `ignore_pretraining_limits=True`，因此 full 行应作为 constrained reference result 呈现。
- `LightGBM` 和 `XGBoost` 是 fixed strong baselines，不是 tuned SOTA baselines。

### 结论

Phase 5 完整 train-size scalability 实验通过。
当前主线已经更完整地覆盖了不同训练规模下的 classification metrics 和 runtime 变化。

### 产出文件

- `src/phase5_scalability_compare.py`
- `results/phase5_scalability_compare.csv`
- `results/phase5_scalability_compare_summary.csv`

### 下一步

- 可以进入 Phase 5 的图表/报告骨架整理：
  - 生成 size-vs-metric 图表
  - 生成 size-vs-runtime 图表
  - 建立英文报告和 PPT 的主线结果结构
- Big Plus 仍然顺延，不在图表/报告骨架整理前抢占主线收尾。

---

## 实验 011：Phase 5 主线图表与报告/PPT 骨架整理

### 日期

2026-04-26

### 阶段归属

- 这是 Phase 5 第三步：主线图表和报告/PPT 骨架整理
- 不改变 Big Plus 方向
- 不新增模型
- 不调参
- 不扩展到 regression 或 survival analysis

### 实验目的

Phase 5 第三步把已完成的主线实验结果整理成可用于英文报告和 15 分钟展示的图表与结构化叙事。

本步骤不产生新的模型训练结果，而是把已有 Phase 4/5 结果转化为可复用的英文图表和报告/PPT 结构。

### 数据来源

- 主线比较结果：
  - `results/phase4_mainline_compare_summary.csv`
- train-size scalability 结果：
  - `results/phase5_scalability_compare_summary.csv`

### 图表生成设置

- 脚本：
  - `src/phase5_make_mainline_figures.py`
- 输入：
  - `results/phase5_scalability_compare_summary.csv`
- 输出目录：
  - `results/figures/`
- 图表格式：
  - PNG
  - PDF
- 每张图使用两个 subplot：
  - `Adult`
  - `Bank Marketing`
- x 轴 train-size 顺序：
  - `512`
  - `2048`
  - `8192`
  - `10000`
  - `full`

### 生成图表

- `results/figures/phase5_scalability_accuracy.png`
- `results/figures/phase5_scalability_accuracy.pdf`
- `results/figures/phase5_scalability_balanced_accuracy.png`
- `results/figures/phase5_scalability_balanced_accuracy.pdf`
- `results/figures/phase5_scalability_macro_f1.png`
- `results/figures/phase5_scalability_macro_f1.pdf`
- `results/figures/phase5_scalability_total_seconds_median.png`
- `results/figures/phase5_scalability_total_seconds_median.pdf`

### 报告和 PPT 骨架

- 英文报告骨架：
  - `report/outline.md`
- 15 分钟英文展示骨架：
  - `slides/outline.md`

### 主线观察

- `Adult` 上树模型整体更强，`TabICL` 接近树模型，`TabPFN v2` 相对弱且慢。
- `Bank Marketing` 上 foundation models 表现更亮，尤其 `TabICL` 在 `balanced_accuracy` 和 `macro_f1` 上更有优势。
- train size 增大时，多数指标提升，`Bank Marketing` 上提升尤其明显。
- runtime 随 train size 增大而上升，foundation models 增幅明显；`TabICL` 明显快于 `TabPFN v2`。

### Caveats

- runtime caveat：树模型在 CPU 上运行，foundation models 可能使用 CUDA，因此这是 practical mixed-device timing，不是严格同设备公平速度比较。
- split caveat：实验使用 repeated stratified splits；每个 seed 内模型共享同一 split，但跨 seeds 不是同一个固定测试集。
- baseline caveat：`LightGBM` 和 `XGBoost` 是 fixed strong baselines，不是 tuned SOTA baselines。
- full-reference caveat：`full` train size 是工程参考结果；其中 `TabPFN v2` 超过更干净的 10k 支持范围口径。

### 结论

Phase 5 第三步已经完成。当前主线已经覆盖主线模型比较、额外分类指标、train-size scalability、runtime 分析、模型优缺点和报告/PPT 骨架，可以独立支撑课程报告。

### 下一步

- Phase 6 方法冻结/设计已完成
- Phase 6 Adult 实验脚本和 smoke test 已在实验 012 完成
- Big Plus 仍然保持为 `TabICL` 支持集选择方向

---

## 实验 012：Phase 6 Adult + TabICL 支持集选择 smoke test

### 日期

2026-04-26

### 阶段归属

- 这是 Phase 6 的脚本实现 smoke test
- 只用于确认四种支持集策略、结果 schema 和关键支持集字段能正常写出
- 不作为完整 Adult 主实验结果
- 不作为 Big Plus 成功或失败的正式结论

### 实验目的

实现并验证 `src/phase6_big_plus_adult.py`：

- 只使用 `Adult`
- 只使用 `TabICL`
- 实现四种已冻结支持集策略
- 先跑 `budget=512, seed=42` smoke test
- 不启动完整长实验

### 数据集

`Adult`（OpenML，本地缓存）

### 模型

- `TabICL`

### 支持集策略

- `Full Context`
- `Random Subset`
- `Balanced Random Subset`
- `Balanced Prototype Retrieval`

### 实验设置

- seed：`42`
- budget：`512`
- split protocol：seed 内固定的 stratified train/test split
- `Full Context` 使用完整训练 split，作为 budget-independent reference
- 其他三种策略使用相同 `requested_budget = 512`

### 命令

```bash
python3 src/phase6_big_plus_adult.py --budgets 512 --seeds 42
```

### 评价指标

- `accuracy`
- `balanced_accuracy`
- `macro_f1`
- `fit_seconds`
- `predict_seconds`
- `total_seconds`

### 支持集记录字段

已确认 detail CSV 中包含并写出：

- `requested_budget`
- `actual_support_size`
- `support_class_counts`

summary CSV 中也包含支持集聚合字段：

- `requested_budget_min`
- `requested_budget_max`
- `actual_support_size_min`
- `actual_support_size_max`
- `support_class_counts`

### 输出文件

- `results/phase6_big_plus_adult.csv`
- `results/phase6_big_plus_adult_summary.csv`

### 完整性校验

- detail CSV：`4` 行
- summary CSV：`4` 行
- 四种策略均出现
- `requested_budget` 无缺失
- `actual_support_size` 无缺失
- `support_class_counts` 无缺失

### Smoke test 结果

| strategy | budget | requested_budget | actual_support_size | support_class_counts | accuracy | balanced_accuracy | macro_f1 | total_seconds |
| --- | --- | ---: | ---: | --- | ---: | ---: | ---: | ---: |
| full_context | full | 39073 | 39073 | `{"<=50K": 29724, ">50K": 9349}` | 0.8729 | 0.7946 | 0.8135 | 235.5895 |
| random_subset | 512 | 512 | 512 | `{"<=50K": 410, ">50K": 102}` | 0.8402 | 0.7068 | 0.7381 | 13.5195 |
| balanced_random_subset | 512 | 512 | 512 | `{"<=50K": 256, ">50K": 256}` | 0.7870 | 0.8159 | 0.7532 | 36.6981 |
| balanced_prototype_retrieval | 512 | 512 | 512 | `{"<=50K": 256, ">50K": 256}` | 0.6967 | 0.7052 | 0.6540 | 8.4308 |

### 观察

- 脚本已能完整运行四种支持集策略。
- `Balanced Random Subset` 与 `Balanced Prototype Retrieval` 的类别配额均为 `256/256`，符合冻结设计。
- `Random Subset` 保留了随机抽样后的自然类别比例，本次为 `410/102`。
- `Full Context` 本次预测耗时明显长于预算受限策略，因此完整 Adult 主实验启动前需要显式确认。
- 这只是单 seed、单 budget 的 smoke test，不能据此判断 `Balanced Prototype Retrieval` 是否有效。

### 结论

Phase 6 脚本实现和 smoke test 通过。
结果表 schema 已经满足后续完整 Adult 主实验的基本记录需求。

### 下一步

- 审查 `src/phase6_big_plus_adult.py`
- 确认后运行完整 Adult 主实验：
  - budgets：`512`、`2048`、`8192`
  - seeds：`42`、`43`、`44`
  - strategies：四种已冻结策略

---

## 实验 013：Phase 6 Adult + TabICL 支持集选择主实验与结果图表

### 日期

2026-04-27

### 阶段归属

- Phase 6 Big Plus Adult 主实验
- 这是 smoke test 之后的正式 Adult-only 支持集选择 ablation
- 没有启动 Bank Marketing 次验证
- 没有重跑 Phase 4/5 主线
- 没有启动 Phase 7

### 实验目的

在冻结方法不变的前提下，验证四种 `TabICL` 支持集策略在 Adult 上的表现、runtime 和预算公平对比关系。

重点问题：

- 预算受限支持集能否接近 `Full Context`？
- `Balanced Prototype Retrieval` 是否优于 `Random Subset` 和 `Balanced Random Subset`？
- 支持集压缩是否显著降低 runtime？

### 数据集

`Adult`（OpenML，本地缓存）

### 模型

- `TabICL`

### 支持集策略

- `Full Context`
- `Random Subset`
- `Balanced Random Subset`
- `Balanced Prototype Retrieval`

### 实验设置

- seeds：`42`, `43`, `44`
- budgets：`512`, `2048`, `8192`
- split protocol：每个 seed 内使用 stratified train/test split
- `Full Context` 使用完整训练 split，`actual_support_size = 39073`
- 三种 budget-limited 策略在同一 `budget/seed` 下共享相同 `requested_budget`

### 输出文件

- `results/phase6_big_plus_adult.csv`
- `results/phase6_big_plus_adult_summary.csv`
- `results/figures/phase6_big_plus_adult_accuracy.png`
- `results/figures/phase6_big_plus_adult_balanced_accuracy.png`
- `results/figures/phase6_big_plus_adult_macro_f1.png`
- `results/figures/phase6_big_plus_adult_total_seconds_median.png`
- `results/figures/phase6_big_plus_adult_bpr_delta.png`
- `report/phase6_big_plus_results.md`
- `report/phase6_big_plus_results_zh.md`

### 完整性校验

- detail CSV：`30` 行
- summary CSV：`10` 行
- detail 和 summary 都包含：
  - `requested_budget`
  - `actual_support_size`
  - `support_class_counts`
- 三个 budget-limited 策略在同一 `budget/seed` 下 `requested_budget` 一致
- 所有运行设备记录为 `cuda`

### 结果摘要

| strategy | budget | accuracy_mean | balanced_accuracy_mean | macro_f1_mean | total_seconds_median |
| --- | --- | ---: | ---: | ---: | ---: |
| full_context | full | 0.8722 | 0.7919 | 0.8117 | 45.8005 |
| random_subset | 512 | 0.8438 | 0.7358 | 0.7592 | 3.4771 |
| random_subset | 2048 | 0.8573 | 0.7668 | 0.7873 | 2.5291 |
| random_subset | 8192 | 0.8654 | 0.7874 | 0.8038 | 4.6601 |
| balanced_random_subset | 512 | 0.7964 | 0.8180 | 0.7610 | 3.4701 |
| balanced_random_subset | 2048 | 0.8155 | 0.8295 | 0.7792 | 2.5361 |
| balanced_random_subset | 8192 | 0.8344 | 0.8293 | 0.7941 | 4.6720 |
| balanced_prototype_retrieval | 512 | 0.7020 | 0.7093 | 0.6588 | 3.2666 |
| balanced_prototype_retrieval | 2048 | 0.7336 | 0.7684 | 0.7002 | 2.4829 |
| balanced_prototype_retrieval | 8192 | 0.6437 | 0.7256 | 0.6253 | 4.7904 |

### BPR 对比

- `Balanced Prototype Retrieval` 没有优于 `Balanced Random Subset`：所有 budget 和所有指标都是负差值。
- 相对 `Random Subset`，只有 `budget=2048` 的 balanced accuracy 有极小正差值：`+0.0016`。
- 在 accuracy 和 macro-F1 上，`BPR` 明显低于两个随机 baseline。

### 观察

- `Random Subset` 在 accuracy 和 macro-F1 上最稳，随 budget 增大接近 `Full Context`。
- `Balanced Random Subset` 在 balanced accuracy 上最强，说明类别平衡本身是强 baseline。
- `Balanced Prototype Retrieval` 的“类中心原型”假设在 Adult 上不成立，至少当前冻结定义没有带来性能收益。
- 预算受限策略的 median runtime 约 `2.5s` 到 `4.8s`，明显低于 `Full Context` 的 `45.8005s`。

### 结论

Phase 6 Adult 主实验给出一个有价值的负结果：

> 支持集压缩能显著降低 `TabICL` runtime，但当前冻结版 `Balanced Prototype Retrieval` 没有超过强随机 baseline。

报告中应把 Phase 6 写成 support-set selection ablation，而不是成功的新方法。
后续如果继续探索检索方法，必须作为新的方法版本，并明确击败 `Balanced Random Subset`。

### 下一步

- 继续 Phase 6 论文/报告材料整理
- 打磨 figure captions、结果表和中英文摘要
- 不启动 Phase 7
- 不回改冻结方法

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
