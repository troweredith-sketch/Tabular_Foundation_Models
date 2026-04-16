# Tabular Foundation Models

这是一个面向课程项目的学习型仓库，主题是比较表格基础模型与传统树模型在中小型表格分类任务上的表现。

## 当前阶段

目前已完成第一阶段内容：

- 明确项目问题
- 学习 6 个基础概念
- 搭建本地实验环境
- 完成第一份教学 notebook

当前项目问题：

> We compare tabular foundation models with boosted-tree baselines on small to medium tabular classification datasets.

## 计划比较的模型

- TabPFN v2
- TabICL
- XGBoost
- LightGBM

## 初步选择的数据集

- Adult
- Bank Marketing
- Credit-G

## 当前仓库内容

- `notebooks/phase1_concepts_demo.ipynb`：第一阶段中文教学 notebook
- `docs/project_record.md`：项目整体进度与里程碑记录
- `docs/work_log.md`：按时间记录每天/每次推进内容
- `docs/experiment_log.md`：按实验记录数据集、模型、结果与观察
- `src/`：后续实验代码
- `data/`：数据目录
- `results/`：实验结果
- `report/`：英文报告
- `slides/`：演示文稿

## 本地环境

建议在 WSL Ubuntu 中使用项目本地虚拟环境：

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements-basic.txt
```

## 下一步

下一阶段将开始加载真实表格分类数据集，并先跑通一个 baseline 模型。

## 如何记录项目过程

为了方便后续回顾、展示和写报告，建议每次推进都同步更新下面 3 份文件：

1. `docs/project_record.md`
   用来维护项目整体阶段、当前状态和关键里程碑。
2. `docs/work_log.md`
   用来记录每次学习、调试、阅读、写代码、搭环境时做了什么。
3. `docs/experiment_log.md`
   用来记录每次实验的设置、结果和观察，后面写报告时会非常有用。
