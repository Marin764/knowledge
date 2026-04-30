---
trigger: always_on
---

# Game Design Wiki - Schema Hub

这是知识库的"路由器"。AI 必须遵循以下红线，并根据任务加载对应的 Skill 文件。

## 0. 启动读档 (Initialization) 
每次新对话，按顺序静默读取：

| 优先级 | 文件 | 目的 |
| :--- | :--- | :--- |
| ① 最高 | `MEMORY.md` | 当前进度、未完成任务、用户偏好 |
| ② 高 | `decisions/INDEX.md` | 已生效的架构决策摘要 |
| ③ 中 | `wiki/log.md` 最近5条 | 上次做了什么 |
| ④ 按需 | `wiki/index.md` | 页面全景（查询任务时读） |

> **读档是静默行为**，不向用户汇报"我正在读取..."。

## 1. 核心红线 (The Red Lines)
- **不可篡改 raw/**：该目录仅供读取，严禁修改或删除。
- **强制中文文件名**：所有 wiki 页面文件名必须为中文。
- **单步串行**：处理 ingest 时必须逐篇处理，严禁并行读取多文件。
- **矛盾不擅裁**：发现来源冲突时，标注 `⚠️ 待裁定`，不自行判断对错。

## 2. 目录原则 (Structural Base)
- `wiki/`：AI 维护的知识页面（games, concepts, mechanics, analysis, source）。
- `raw/`：原始只读资料（文章、截图）。
- `assets/`：工业级标准化资产库（JPEG/GIF）。
- `skills/`：**任务说明书（AI 执行前必读）**。
- `decisions/`：**架构决策记录 (ADR)**。
- `MEMORY.md`：项目状态与用户偏好（根目录）。

## 3. 工作流分流 (Skill Routing)

| 场景 | 动作 | 需加载的子规范 (Mandatory) |
| :--- | :--- | :--- |
| **写作/创建页面** | 任何 Markdown 写入 | `skills/05-hygiene_rules.md` |
| **更新 Frontmatter** | 处理页面元数据 | `skills/00-metadata_schema.md` |
| **资料摄入 (Ingest)** | `处理 <file>` | `skills/04-ingest_workflow.md` |
| **UI 视觉分析** | `分析UI <image>` | `skills/01-ui_analysis.md` |
| **批量截图处理** | 整理原始截图包 | `skills/03-batch_image_ingest.md` |
| **生成系统规范** | 编写交互 Spec | `skills/02-game_system_ux_spec.md` |

## 4. 收尾协议 (Closing Protocol)
每次写入操作完成后，按顺序执行：

1. **更新 MEMORY.md**：同步当前进度与下一步计划。
2. **写 ADR**：如触发条件成立（引入新架构/改动逻辑），存入 `decisions/`。
3. **更新索引**：运行 `node scripts/internal/lint.js` 并更新 `wiki/log.md`。
4. **简明汇报**：创建/更新了哪些页面，是否有矛盾。

### ADR 触发条件
- 引入新的目录结构或文件类型。
- 修改任何 Skill 文件的核心逻辑。
- 推翻或修正现有的红线规则。
- 建立跨游戏的新分析框架（如星铁 16 帧提取法）。

## 5. 自动化工具 (CLI)
- **健康检查**：`node scripts/internal/lint.js`
- **生成幻灯片**：`bash scripts/wiki.sh slides --all`

---
*Schema version: 2.1 | Last updated: 2026-04-23*