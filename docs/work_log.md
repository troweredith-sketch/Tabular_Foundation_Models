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

## 2026-04-22（第三阶段启动）

### 花费时间

约 1 个工作阶段

### 目标

正式进入第三阶段，接入 `TabPFN v2`，并在固定 Adult 测试集上与 `LightGBM` 做第一次正式对比。

### 实际完成内容

- 检查并复用第二阶段的 Adult baseline notebook 逻辑
- 在项目本地 `.venv` 中安装 `tabpfn`
- 新增可复现实验脚本：`src/phase3_adult_compare.py`
- 复用 Adult 本地缓存和 `random_state=42` 的固定训练/测试集划分
- 在同一测试集上运行 `LightGBM` 和 `TabPFN v2`
- 生成结果文件：`results/phase3_adult_compare.csv`
- 将第三阶段第一次正式对比的结果同步写回项目记录

### 遇到的问题

- `TabPFN v2` 默认不接受当前 Adult 全量训练集规模
- 报错提示官方支持上限为 `10,000` 个样本，而当前训练集大小是 `39,073`

### 解决方式

- 保持训练/测试集划分不变
- 在 `TabPFN v2` 实验里显式设置 `ignore_pretraining_limits=True`
- 同时把这个限制条件写进脚本说明和实验记录，而不是把它隐藏掉

### 学到的东西

- 第三阶段除了比较准确率，还要记录模型能不能顺利接入、有哪些真实限制
- `TabPFN v2` 在这个任务上不是“装好就直接公平比较”，它对数据规模有明确前提
- 即使有 GPU，实际预测耗时也可能远高于树模型，因此运行成本本身就是结果的一部分

### 下一步

- 做一个训练样本不超过 `10,000` 的 Adult 控制实验
- 判断当前全量 Adult 结果在报告里应该如何表述
- 再决定是否继续扩展到下一数据集或模型

---

## 2026-04-23（路线升级与双轨规划）

### 花费时间

约 1 次规划重构

### 目标

- 判断当前项目方向是否需要修改
- 决定是否挑战 Big Plus
- 把后续阶段、文档同步规则和学习型沉淀规则一次性定清楚

### 实际完成内容

- 重新阅读项目要求，并对照当前仓库进度判断方向是否需要改轨
- 确认项目主方向不变，但推进方式升级为“双轨推进”
- 确定 Big Plus 主方向为：基于 `TabICL` 的检索式支持集选择改进
- 重写 `docs/phase_plan.md`，把当前阶段重定义为“主线口径修正与公平性加固”
- 新增 `docs/big_plus_plan.md`，作为 Big Plus 正式说明文档
- 更新 `docs/project_record.md` 和 `docs/session_handoff.md`
- 新增当前阶段学习型文档：`notebooks/phase3_fairness_reset.md`
- 确认从现在起每推进一个阶段，都要在 `notebooks/` 下新增一篇中文“教学 + 复盘”风格的 `md`

### 遇到的问题

- 原来的阶段计划是单线结构，已经不适合“主线 + Big Plus”并行推进
- 如果直接写未来阶段结果，会让记录看起来像已经完成，和真实状态不一致

### 解决方式

- 保留历史阶段完成记录，不重写真实过去
- 将当前及之后的阶段改成新的双轨结构
- 只为当前已推进的阶段新增正式学习文档，未来阶段先写进路线图，等真正推进时再补对应 `md`

### 学到的东西

- 课程项目一旦开始追求加分项，就必须先把主线和支线分开管理
- 结果的“可运行性”和“可作为主结论的证据强度”必须分开判断
- 如果想让未来的自己继续推进，最有价值的不是堆更多文件，而是让每份文件各司其职

### 下一步

- 完成 Phase 3 的口径修正与统一字段定义
- 设计并执行 `Adult` 控制实验
- 接入 `TabICL`
- 继续推进主线模型与数据集补齐

---

## 2026-04-23（Phase 3 完成）

### 花费时间

约 1 次实验收尾 + 文档同步

### 目标

- 用一个更公平的控制实验把 Phase 3 真正做完
- 统一第三阶段脚本输出字段
- 把实验结论同步写回 `docs/` 和 `notebooks/`

### 实际完成内容

- 将 `src/phase3_adult_compare.py` 轻量重构为单入口双场景脚本
- 新增 `--scenario` 参数，支持：
  - `full_adult_limit_override`
  - `adult_control_10k`
- 统一第三阶段结果字段为固定 schema
- 重新生成 full Adult 受限条件结果
- 新增并运行 `Adult 10k control` 控制实验
- 生成：
  - `results/phase3_adult_compare.csv`
  - `results/phase3_adult_compare_10k.csv`
- 更新 `docs/experiment_log.md`
- 更新 `docs/project_record.md`
- 更新 `docs/session_handoff.md`
- 更新 `docs/phase_plan.md`
- 更新 `README.md`
- 将 `notebooks/phase3_fairness_reset.md` 升级为带真实结果的学习型阶段总结
- 在 `notebooks/phase3_adult_compare_guide.md` 开头补充说明，明确它是过程性指南

### 遇到的问题

- 需要确认 `TabPFN v2` 在 `10,000` 条训练样本时能否不加限制直接运行
- 需要保证控制实验和 full Adult 实验使用同一个测试集

### 解决方式

- 固定 `test_size=0.2`、`random_state=42`、`stratify=y`
- 先切固定测试集，再从原训练集内部抽 `10,000` 条样本做控制实验
- 在 `10,000` 条设置下直接运行成功，没有触发 `9,500` fallback

### 学到的东西

- 公平性修正不是删除旧结果，而是补上能解释旧结果的控制实验
- 控制实验最重要的是“只改一个关键条件”，这里改的是训练样本规模
- 结果字段一旦统一，后面 Phase 4 和写报告都会轻松很多

### 下一步

- 进入 Phase 4
- 在 `Adult` 上接入 `TabICL`
- 把 `XGBoost` 补进统一主线比较
- 将主线扩展到 `Bank Marketing`

---

## 2026-04-23（Phase 3 升级：多 seed 稳定性评估）

### 花费时间

约 1 次脚本重构 + 1 轮完整多 seed 运行 + 文档回填

### 目标

- 把 Phase 3 从“单次结果”升级成“多次运行后的稳定结论”
- 修复 `phase3_adult_compare.py` 直接运行时只执行 full Adult 的问题
- 让脚本默认同时跑 `full Adult` 和 `10k control`

### 实际完成内容

- 将 `src/phase3_adult_compare.py` 的 CLI 改成：
  - `--scenario all`
  - `--scenario full_adult_limit_override`
  - `--scenario adult_control_10k`
- 将默认行为改成直接运行时执行 `all`
- 新增 `--seeds` 参数，默认 `42 43 44 45 46`
- 把结果文件升级为多 seed 行级明细：
  - `results/phase3_adult_compare.csv`
  - `results/phase3_adult_compare_10k.csv`
- 新增汇总文件：
  - `results/phase3_adult_compare_summary.csv`
- 真实运行完成 `5 seeds × 2 scenarios × 2 models`
- 更新 `docs/experiment_log.md`，新增实验 005
- 更新 `docs/project_record.md`
- 更新 `docs/session_handoff.md`
- 更新 `docs/phase_plan.md`
- 更新 `README.md`
- 更新 `notebooks/phase3_fairness_reset.md`
- 更新 `notebooks/phase3_adult_compare_guide.md`

### 遇到的问题

- 旧版脚本默认 `--scenario = full_adult_limit_override`，所以直接运行时只会得到 full Adult 结果
- 单次结果更适合做锚点，不适合直接当最终统计结论
- 如果只重跑一个场景，summary 还需要能够从现有结果文件重新聚合

### 解决方式

- 把默认入口改成 `all`
- 让脚本在每个 seed 上重新做一次 split / subset，而不是机械重复同一条命令
- summary 统一从现有明细文件聚合生成

### 学到的东西

- 对课程项目来说，最有价值的重复实验是“多 seed / 多抽样”，而不是简单重复同一设置
- `accuracy` 更适合报告 `mean ± std`，运行时间更适合报告 `median`
- 一个脚本如果默认行为和文档不一致，很容易让后续自己误判项目状态

### 下一步

- Phase 3 已经可以封箱，后续默认引用 `results/phase3_adult_compare_summary.csv`
- 进入 Phase 4
- 在 `Adult` 上接入 `TabICL`
- 把 `XGBoost` 补进统一主线比较
- 将主线扩展到 `Bank Marketing`

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
