# ADR 018：将批量截图 Skill 扩展为 atlas 主链

- Status: accepted
- Date: 2026-04-27

## Context

`skills/03-batch_image_ingest.md` 原先只覆盖：

`raw/screenshots -> mapping_log -> assets/<game>_ui -> wiki/analysis`

但知识库当前的实际 UI 生成主链已经扩展为：

`assets/<game>_ui -> metadata/screens -> crops/review -> metadata/atlas -> atlas`

也就是说，批量截图处理不再只服务于“原型图确权”和“分析写作”，还要服务于后续 AI 界面生成、风格重构和控件语法学习。

如果 Skill 03 不更新，执行者会停在 `assets/<game>_ui/`，忽略已经稳定运行的控件拆解与图谱固化层。

## Decision

将 `skills/03-batch_image_ingest.md` 正式扩展为“两段式主链”：

1. 第一段：原型截图确权  
   `raw/screenshots -> mapping_log -> assets/<game>_ui`

2. 第二段：控件图谱化  
   `assets/<game>_ui -> metadata/screens -> crops/review -> metadata/atlas -> atlas`

并明确：

- 当目标包含 AI 生成界面、风格重构、控件语法学习时，第二段为必选。
- atlas 是 AI 主参考层，高于单张原图和历史单控件实验层。
- `generated/` 继续只作历史实验归档，不回到主链。

## Consequences

正面影响：

- 批量截图处理、UI 分析、界面生成三条链路重新对齐。
- 执行者会把 atlas 图谱视为正式产物，而不是临时扩展。
- 后续原神或其他游戏扩展到控件图谱层时，有统一方法可沿用。

代价与约束：

- Skill 03 的执行成本提高，不再只是“筛图 + 改名”。
- 当任务仅需分析、不需生成时，必须明确是否停在 `assets/<game>_ui/`。
