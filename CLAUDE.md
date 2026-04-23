# Game Design Wiki - Schema Hub

这是知识库的“路由器”。AI 必须遵循以下红线，并根据任务加载对应的 Skill 文件。

## 1. 核心红线 (The Red Lines)
- **不可篡改 raw/**：该目录仅供读取，严禁修改或删除。
- **强制中文文件名**：所有 wiki 页面文件名必须为中文。
- **单步串行**：处理 ingest 时必须逐篇处理，严禁并行读取多文件。
- **真相源优先**：涉及原神等截图分析，必须先查阅 `raw/screenshots/mapping_log.md`。

## 2. 目录原则 (Structural Base)
- `wiki/`：AI 维护的知识页面（games, concepts, mechanics, analysis, source）。
- `raw/`：原始只读资料。
- `assets/`：工业级标准化资产库（JPEG/GIF）。
- `skills/`：**任务说明书（AI 执行前必读）**。
- `scripts/`：自动化工具集。

## 3. 工作流分流 (Skill Routing)

AI 在执行以下任务前，**必须先读取对应的子规范**：

| 场景 | 动作 | 需加载的子规范 (Mandatory) |
| :--- | :--- | :--- |
| **写作/创建页面** | 任何 Markdown 写入 | `skills/05-hygiene_rules.md` (命名/链接/质量) |
| **更新 Frontmatter** | 处理页面元数据 | `skills/00-metadata_schema.md` (YAML 模板) |
| **资料摄入 (Ingest)** | `处理 <file>` | `skills/04-ingest_workflow.md` (翻译/层级/索引) |
| **UI 视觉分析** | `分析UI <image>` | `skills/01-ui_analysis.md` (五维度分析框架) |
| **批量截图处理** | 整理原始截图包 | `skills/03-batch_image_ingest.md` (确权/映射日志) |
| **生成系统规范** | 编写交互 Spec | `skills/02-game_system_ux_spec.md` (Spec 骨架) |

## 4. 自动化工具 (CLI)
- **健康检查**：运行 `bash scripts/wiki.sh lint`。
- **生成幻灯片**：运行 `bash scripts/wiki.sh slides --all`。
- **详情参考**：`scripts/README.md`。

---
*Schema version: 2.0 (Modular) | Last updated: 2026-04-23*