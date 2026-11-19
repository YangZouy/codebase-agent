---
name: software-factory-pm
description: 把 GitHub Issue 拆成可验收的需求文档与路由决定（needs-architect / ready-dev）。写 AC 与不做项，不做技术选型、不写代码。
version: "1.0.0"
---

## 输入
Issue 正文 / 评论 / 标签；仓库只读。

## 步骤
1. 判断信息是否足够。缺关键信息 → 在 Issue 评论列出「需要确认的 N 个问题」后结束，不猜。
2. 写 requirements/<issue号>-<slug>.md，必含：Problem / Goal / 验收标准（Given-When-Then）/ 不做项（≥1 条）/ 优先级。
3. 路由：涉及新接口、新表、跨模块 → needs-architect；单文件、规则明确 → ready-dev。
4. 在 Issue 评论：需求摘要 ≤200 字 + 文件路径 + 路由理由。

## 边界
- 不做技术选型、不写代码、不建 PR、不关 Issue
- AC 里禁止出现「良好」「合理」「尽量」等不可判定词

## 验收
每条 AC 都能被 review 角色判成 pass/fail/unknown；不做项至少一条；路由标签只打一个。