# 项目过程日志

这份文档按时间记录每次学习、调试、写代码和推进项目时做了什么。

建议每次记录都尽量包含：

- 日期
- 花费时间
- 目标
- 实际完成内容
- 遇到的问题
- 解决方式
- 学到的东西
- 下一步

---

## 2026-04-16

### 花费时间

约 1 个工作阶段

### 目标

完成项目第一阶段，建立学习和实验的起点。

### 实际完成内容

- 明确项目问题和研究范围
- 选择第一阶段的学习顺序
- 学习 `classification`、`train/test split`、`accuracy`、`overfitting`、`categorical features`、`missing values`
- 完成一个使用 `breast_cancer` 数据集的教学实验
- 搭建本地 `.venv`
- 安装 `jupyterlab`、`numpy`、`pandas`、`scikit-learn`、`openml`、`xgboost`、`lightgbm`
- 创建中文 notebook：`notebooks/phase1_concepts_demo.ipynb`
- 初始化 Git 仓库并推送到 GitHub
- 建立项目记录体系：`project_record.md`、`work_log.md`、`experiment_log.md`
- 读取并修订外部的初步阶段计划
- 新增项目记忆卡 `session_handoff.md`

### 遇到的问题

- `jupyter` 初始未安装
- `lightgbm` 安装后缺少系统运行库 `libgomp.so.1`
- WSL 里 `gh auth login` 无法自动打开浏览器

### 解决方式

- 在项目虚拟环境中安装 `jupyterlab`
- 安装系统库 `libgomp1`
- 手动打开 GitHub device login 页面完成 `gh` 登录

### 学到的东西

- 训练集和测试集必须区分，不然很难判断泛化能力
- 训练集准确率非常高时，需要警惕过拟合
- 环境搭建过程本身也是项目推进的一部分，值得记录
- 如果把关键信息沉淀到仓库文件里，就不用依赖超长对话记忆

### 下一步

- 进入第二阶段
- 加载第一个真实表格分类数据集
- 跑通一个 baseline 模型
- 每次推进后同步更新记忆卡和日志

---

## 2026-04-16（第二阶段推进）

### 花费时间

约 1 个工作阶段

### 目标

进入第二阶段，在第一个真实表格数据集上跑通 baseline。

### 实际完成内容

- 选定 `Adult` 作为第一个真实数据集
- 从 `OpenML` 成功加载数据
- 检查样本数、特征数、目标分布、类别特征和缺失值
- 确认 `workclass`、`occupation`、`native-country` 存在缺失值
- 确认该数据集有 8 个类别特征、6 个数值特征
- 使用 `LightGBM` 完成第一个 baseline
- 编写 `notebooks/phase2_adult_baseline.ipynb`
- 生成 `results/first_result.csv`
- 更新项目计划、记忆卡和项目记录

### 遇到的问题

- notebook 通过 `nbconvert` 执行时，结果文件保存到错误的相对路径

### 解决方式

- 修改 notebook 中的保存逻辑，让它先判断项目根目录，再写入 `results/first_result.csv`

### 学到的东西

- 第二阶段的重点是建立第一条正式实验链路，而不是立刻追求最高分
- 真实数据集实验前，必须先做列类型、缺失值和目标分布检查
- 相对路径在 notebook 和自动执行环境里可能不一致，需要写得更稳妥

### 下一步

- 进入第三阶段
- 接入 `TabPFN v2`
- 在 Adult 数据集上与 LightGBM 做第一次正式对比

---

## 2026-04-22（第二阶段收尾确认）

### 花费时间

约 1 次阶段复盘

### 目标

确认第二阶段已经完成，并把项目记录正式同步到“进入第三阶段”的状态。

### 实际完成内容

- 复查项目记忆卡和项目总记录
- 确认第二阶段目标已经达成：第一个真实数据集实验和 baseline 已完成
- 将 `project_record.md` 中的阶段状态更新为“Phase 2 已完成，Phase 3 进行中”
- 将第二阶段的正式完成时间同步到当前日期
- 补充工作日志和实验日志中的阶段归属说明

### 遇到的问题

- 文档中之前已经记录“第二阶段已完成”，但缺少“2026-04-22 正式确认收尾”的痕迹

### 解决方式

- 在 `project_record.md` 和 `work_log.md` 中补写阶段收尾确认记录
- 在 `experiment_log.md` 中明确 Adult baseline 是 Phase 2 的官方基线实验

### 学到的东西

- 阶段“实验跑通”和阶段“正式收尾确认”是两件相关但不完全相同的事
- 在项目推进中，阶段状态最好和当前日期保持一致，方便回顾和展示

### 下一步

- 进入第三阶段
- 接入 `TabPFN v2`
- 在 Adult 数据集上与 LightGBM baseline 做第一次正式对比

---

## 记录模板

### 日期

YYYY-MM-DD

### 花费时间

X 小时

### 目标

- 

### 实际完成内容

- 

### 遇到的问题

- 

### 解决方式

- 

### 学到的东西

- 

### 下一步

- 
