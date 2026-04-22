# Skills Index (技能库)

> 本目录存放供 AI 使用的**标准化工作 Skill（技能文件）**。
>
> 每个 Skill 是一份完整的"任务说明书"，告知 AI 在特定场景下应采用的分析框架、输出格式与质量检查标准。

---

## 现有 Skills 列表

| 编号 | 文件 | 触发场景 | 输出目标 |
|------|------|------|------|
| 01 | [01-ui_analysis.md](01-ui_analysis.md) | 用户提供 UI 截图，要求进行交互分析 | 生成结构化 Markdown 分析报告并录入 `wiki/analysis/` |
| 02 | [02-game_system_ux_spec.md](02-game_system_ux_spec.md) | 用户要求生成任意游戏系统的交互规范（战令、商城、抽卡等） | 生成正式规范文档并保存至 `exports/` |
| 03 | [03-batch_image_ingest.md](03-batch_image_ingest.md) | 用户提供大批量（≥20张）命名混乱的游戏截图，需要批量归档与分类 | 完成重命名、系统聚类、分析排期，并驱动后续 Skill 01 执行 |

---

## Skill 命名规范

- 文件名格式：`[序号]-[功能标识].md`
- 编号从 `01` 开始，两位数字补零。
- 功能标识使用小写英文 + 下划线。

## 调用规则

AI 在执行以下类型任务时，**必须优先读取对应 Skill 文件**：

- 分析游戏截图（单张/少量有序） → 加载 `01-ui_analysis.md`
- 生成系统交互规范 → 加载 `02-game_system_ux_spec.md`
- 批量摄入大量无序截图（≥20张）→ 加载 `03-batch_image_ingest.md`，**禁止跳过直接分析**
