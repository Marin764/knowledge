# ADR 007: 将游戏 UI 生成 Prompt 模板独立为 Skill

## 背景
在生成游戏界面时，AI 如果只收到“用 HTML/Figma 做一个界面”这类泛指令，容易默认落入网页布局语法，产出偏 dashboard、landing page 或标准 web card 的结果。此前相关约束分散在对话解释和临时提示中，缺乏可复用的固定模板。

## 决策
1. **新增独立 Skill**：创建 `skills/06-game_ui_prompt_template.md`，专门负责“生成游戏 UI Prompt / 界面 Brief”。
2. **将反网页化约束模板化**：把“先声明媒介、先写禁止项、先锁 16:9 构图、再写模块和状态”的提示骨架固化为 Skill。
3. **接入路由层**：在 `AGENTS.md`、`CLAUDE.md`、`rules.md` 的 Skill Routing 中新增“生成游戏 UI Prompt / 界面稿”场景。
4. **将系统规范作为上游输入**：后续生成游戏 UI Prompt 时，优先从 `skills/02-game_system_ux_spec.md` 和相关 `wiki/analysis/` 页面提取页面、区域、组件、状态。

## 原因 (Why)
- **减少网页味偏移**：把“不要做成网页”的约束前置并模板化。
- **提高复用性**：以后生成回归、战令、签到等游戏界面时，可以直接命中同一套 Prompt 语法。
- **保持知识库结构清晰**：将“为什么会偏网页”“如何写成游戏 UI Prompt”从聊天解释沉淀为正式技能。

## 影响
- 后续凡是编写游戏 UI Prompt、HTML 游戏界面稿 Brief、Figma 游戏界面设计 Brief，都应优先加载本 Skill。
- 技能体系从“分析 / 规范 / 摄入”扩展到“生成提示模板”，形成更完整的下游链路。

## 状态
Accepted (2026-04-24)
