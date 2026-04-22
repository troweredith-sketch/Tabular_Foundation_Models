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
