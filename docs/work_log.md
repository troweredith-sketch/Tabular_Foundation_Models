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

### 下一步

- 进入第二阶段
- 加载第一个真实表格分类数据集
- 跑通一个 baseline 模型

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
