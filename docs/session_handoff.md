# 项目记忆卡

这是一张给后续对话快速续接用的超短记忆卡。

如果新开对话，默认先让 AI 阅读这份文件，再决定是否继续读 `docs/phase_plan.md` 和 `docs/project_record.md`。

## 项目身份

- 项目主题：Tabular Foundation Models
- 项目类型：机器学习课程项目
- 最终交付：英文报告 + 15 分钟演示
- 截止时间：2026-05-04
- 当前学习方式：边学习边实验

## 用户画像

- 机器学习基础：几乎零基础
- 编程基础：会基本 Python，会一点 numpy、pandas、postgresql
- 算力：普通笔记本，必要时可考虑云服务器
- 目标风格：学习成长型
- 可投入时间：每周约 10 小时

## 当前项目范围

- 先只做分类任务
- 计划比较模型：`TabPFN v2`、`TabICL`、`XGBoost`、`LightGBM`
- 初步数据集：`Adult`、`Bank Marketing`、`Credit-G`
- 当前重点指标：`accuracy`、`runtime`、`dataset size sensitivity`

## 当前进度

- 第 1 阶段已完成
- 第 2 阶段已完成
- 第 3 阶段已开始
- 已完成基础概念学习和教学实验
- 已搭建本地 `.venv` 和基础依赖
- 已创建并推送 GitHub 公开仓库
- 已完成第一个真实数据集实验：`Adult + LightGBM baseline`
- 当前状态：第 3 阶段进行中，正在准备接入 `TabPFN v2` 并在同一测试集上做第一次正式对比

## 必读文件

1. `docs/session_handoff.md`
2. `docs/phase_plan.md`
3. `docs/project_record.md`
4. `docs/work_log.md`
5. `docs/experiment_log.md`

## 高优先级原则

- 优先帮助用户理解，而不是只给结果
- 尽量一边讲解，一边做实验
- 每推进一步，就把记录写回仓库
- 不要重复让用户解释已经写进文档里的背景

## 当前推荐下一步

1. 接入 `TabPFN v2`
2. 在 Adult 数据集上与 LightGBM 做第一次正式对比
3. 保持训练/测试集划分一致
4. 记录模型安装难度、运行时间和准确率
5. 把比较结果写进 `docs/experiment_log.md`

## 常用情景模板

### 1. 新开对话

```text
请先阅读 docs/session_handoff.md、docs/phase_plan.md、docs/project_record.md、docs/work_log.md、docs/experiment_log.md。
先用 5 条总结当前项目状态，再继续帮助我完成下一步。
```

### 2. 完成一个阶段后更新记录

```text
我刚完成了一个阶段。请先阅读 docs/session_handoff.md 和 docs/project_record.md，
然后把本次进展同步更新到 docs/project_record.md、docs/work_log.md 和必要的 docs/experiment_log.md。
最后给我一版“当前状态 + 下一步”的简短总结。
```

### 3. 完成一次实验后更新记录

```text
我刚完成了一次实验。请先阅读 docs/session_handoff.md 和 docs/experiment_log.md，
把这次实验的设置、结果、观察和下一步写进 docs/experiment_log.md，
并同步补充 docs/work_log.md。
```

### 4. 需要短交接摘要

```text
请先阅读 docs/session_handoff.md、docs/project_record.md、docs/work_log.md、docs/experiment_log.md，
然后给我一版短交接摘要，只包含：
1. 当前做到哪一步
2. 最近完成了什么
3. 现在卡在哪里
4. 下一步最优先做什么
```

### 5. 开始今天的工作

```text
请先阅读 docs/session_handoff.md 和 docs/phase_plan.md，
告诉我今天最适合推进的 1-2 个任务，并说明为什么先做它们。
```

### 6. 写报告或做展示前

```text
请先阅读 docs/session_handoff.md、docs/project_record.md、docs/experiment_log.md，
基于当前项目进度，帮我整理一版可以直接转成英文报告/PPT 的结构化要点。
```

## 更新规则

如果项目状态发生变化，优先更新以下 3 项：

1. `当前进度`
2. `当前推荐下一步`
3. `常用情景模板` 是否需要调整
