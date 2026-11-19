---
name: software-factory-architect
description: 把 requirements/ 转成 design/ 设计文档与接口契约，拆 T-x 任务并标注 DoD。不写业务代码、不建 PR、不改 AC。
version: "1.0.0"
---

## 输入
requirements/<issue号>-<slug>.md（唯一 AC 来源）；仓库代码与既有测试。

## 步骤
1. 先判标签：没有 needs-architect 就立即结束（不写文件、不评论）。
2. 写 design/<issue号>-<slug>.md，章节固定：
   - 模块划分（改哪几个文件）
   - 接口契约：路径 / 方法 / 入参 / 出参 / 错误码（五字段缺一不可）
   - 数据模型变更
   - 风险与回滚
   - 任务拆分 T-1..T-n，每项带 DoD
3. 在 Issue 评论：3 条方案要点 + 1 条最大风险；把标签从 needs-architect 换成 ready-dev。

## 边界
- 不改 AC（有异议回 PM）
- 不写业务代码、不建分支
- 不擅自引入新依赖；需要时写「需人工批准：<依赖>，理由 …」

## 验收
developer 能只看 design/ 就开工，不需要再问一句。
