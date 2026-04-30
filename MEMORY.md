# MEMORY - 项目状态

## 当前阶段

- **GitHub 同步策略已调整为忽略 assets**：`.gitignore` 已加入 `assets/`，并将已跟踪的 `assets/genshin_ui/` 图片从 Git 索引移除；后续 GitHub 默认只同步知识库文本、规范、脚本和元规则，标准化视觉资产保留在本地。
- **回归系统三国杀 HUD HTML 原型 V1 已落地**：新增 `exports/回归系统-三国杀HUD界面原型_V1.html`，按回归系统 V5 的 `page.hub` 单页合同实现 16:9 横屏游戏 HUD；直接引用三国杀控件包中的活动 pattern、modal 大框、左侧 tab 参考、武将卡面、势力竖条、阶框、兵种图标、对勾与按钮状态合集，支持左侧入口切换但同屏只显示一个总览承载界面。
- **三国杀新增透明组件已切图并入库**：从 `official_components/武将 势力.png`、`武将 阶框.png`、`兵种图标.png`、`武将卡面.png` 拆分出 `43` 个英文命名透明组件，新增 `components/faction/`、`components/hero-frame/`、`components/troop/`、`components/hero-card/`，并生成 `components/sgs-new-components-contact-sheet-v1.png` 便于快速复核；组件语义已同步到 `metadata/components/sgs-components-for-ai.json` 与 `sgs-official-components.json`。
- **三国杀 UI 组件参考包已分类为 AI 生图读取结构**：`assets/three_kingdoms_kill_controls/` 新增 `components/` 与 `patterns/` 两层，保留 `official_components/` 作为来源区；新增 `metadata/components/sgs-components-for-ai.json`、`metadata/patterns/sgs-patterns-for-ai.json`、`assets/三国杀界面生成说明.md` 和目录说明，明确 agent 读取顺序、组件用途与组合模式。
- **游戏 UI Prompt Skill 已收束为精简版规范联动器**：`skills/06-game_ui_prompt_template.md` 现明确依赖已生成的 `exports/*交互设计规范*.md`，默认采用 `16:9` 且横屏优先但不锁死方向，并把多风格系统的偏好确认改成通用提炼规则。
- **游戏 UI Prompt Skill 已补入手游触控与适配底线**：`skills/06-game_ui_prompt_template.md` 现新增操作热区、相邻间距、安全区、画布尺寸与基础适配约束，并引用 Apple / Android / WCAG 官方最小值作为 Prompt 底线。
- **回归系统规范主入口已统一为 V4**：新建 `exports/回归系统-交互设计规范_V4.md`，合并 V2 的完整页面合同与 V3 的空间构图蓝图；`V2/V3` 已降为历史版本，`V1` 已删除。
- **回归系统生图特化规范 V5 已生成**：新增 `exports/回归系统-交互设计规范_V5.md`，在保留系统级页面地图的同时，强化“单次只生成一个页面”的约束，明确页面选择、风格分支、必须出现/禁止出现与单页 Prompt 模板；`wiki/index.md` 已切到 V5。
- **星铁商店界面原型 V1 已落地**：新增 `exports/星穹铁道-商店界面原型_V1.html`，基于 `hsr-shop-main / hsr-shop-world` 与对应裁切控件生成 16:9 游戏内商店页面，保留左侧分类签、中央大商品舞台与右侧赠礼栏。
- **星铁 UI 资产治理 V1.4（metadata 收束）**：`assets/star_rail_ui/` 下 29 张截图仍保持全量覆盖，截图级 JSON 已统一迁入 `assets/star_rail_controls/metadata/screens/`。
- **控件裁切主链路稳定**：`assets/star_rail_controls/crops/` 当前累计 `169` 个真实裁切控件，按类型分类存放。
- **复核层闭环完成**：`assets/star_rail_controls/review/` 当前共有 `58` 张复核图，对应 29 张来源截图的 `annotated + contact-sheet` 成对输出。
- **星铁图谱主产物稳定**：当前主参考图谱为 [recognized-ui-elements-atlas-v3.png](/C:/Users/hutingrong/Desktop/know/assets/star_rail_controls/atlas/recognized-ui-elements-atlas-v3.png)。
- **新 AI 读取入口已补齐**：新增 [assets/给新AI的星铁界面生成说明.md](/C:/Users/hutingrong/Desktop/know/assets/给新AI的星铁界面生成说明.md)，明确 atlas-first 的阅读顺序、可生成界面范围与风格边界。
- **引入本地 BBox 微调工具**：为了解决前端 AI 识别偏差导致截图裁切不准的问题，新增了 `scripts/images/bbox_editor.py` 可视化纠偏工具，闭环了“机器初筛-人工精修”链路。
- **剑与远征：启程 (AFK Journey) 接入**：开始处理竖屏游戏资产，建立了专属游戏页与首篇视觉分析报告。
- **引入竖屏空间构图模型 (ADR 017)**：针对纵向布局优化了 Spatial Slot 映射。
- **批量截图 Skill 已对齐 atlas 主链**：`skills/03-batch_image_ingest.md` 现已正式覆盖 `assets/<game>_ui -> metadata/screens -> crops/review -> metadata/atlas -> atlas` 的后半段，不再停留在“原型图确权即结束”的旧状态。
- **战令系统分析与规范已按新结构重做**：四篇战令分析页已改为页面矩阵、空间槽位、组件合同和跳转线索导向；新规范已输出为 `exports/战令系统-交互设计规范_V4.md`。
- **目录进一步收敛**：`star_rail_controls` 下的 JSON 已统一收束到 `metadata/screens / metadata/atlas / metadata/generated`，根目录、`atlas/` 和 `generated/` 更干净。
- **试验层已收缩**：透明单控件导出层已退出主流程；当前主路径明确为 `star_rail_ui -> metadata/screens -> crops/review -> metadata/atlas -> atlas`。

## 未完成任务

- [ ] **旧版 exports 回填**：将签到规范继续回填到“页面合同 + 区域合同 + 组件合同 + UI Manifest”新结构。
- [ ] **Clippings 摄入**：`raw/articles/` 中仍有 14 篇待处理 Markdown 剪藏。
- [ ] **Atlas 质量回看**：对 `recognized-ui-elements-atlas-v3` 中过小或语义不强的控件做二轮策展，必要时替换为更有代表性的裁切。
- [x] **AFK Journey 资产整理**：完成 137 张截图的分类与 OCR 索引；提取 12 张核心原型至 `assets/afk_journey_ui/` 并建立 `manifest-afk-core.json`。
- [ ] **跨系统图谱扩展**：后续可按同样方法处理原神或新增星铁页面状态图，但继续坚持 atlas-first，不回到单控件透明导出。
- [x] **新增图生图数据集构建技能**：创建 `skills/07-ui_component_extraction_dataset.md`，规范化组件切图与语义标注工作流。
- [ ] **界面生成回测**：后续可继续用商城 / 战令 / 签到等系统验证 `skills/06-game_ui_prompt_template.md` 的稳定性，并观察“真实裁切图 + HTML 复合舞台”是否适合作为默认高保真产出路径。

## 用户偏好

- **回答风格**：始终使用中文，尽量给出结构化、可追溯的结论。
- **重点游戏**：优先关注原神、崩坏：星穹铁道、王者荣耀。
- **资源目标**：当前资源整理优先服务 AI 识别、参考和生成，不再把“单个透明控件素材库”作为主要方向。
- **原型要求**：如果生成游戏界面原型，优先 16:9 游戏界面语法，不做网页化长滚动表达。

## 最近决策

- [[decisions/004-交互规范转向生成合同.md]]：交互规范主文档转为 AI 可消费的页面生成合同。
- [[decisions/009-游戏-ui-skill-升级为线框原型优先.md]]：Skill 升级为灰白线框 + 可交互原型优先。
- [[decisions/010-引入-ui-控件裁切试验管线.md]]：建立星铁截图 bbox 裁切与复核链路。
- [[decisions/013-引入-ui-atlas-图谱层.md]]：atlas 成为 AI 主参考产物层。
- [[decisions/014-停用-ai-单控件透明层并收束到atlas主产物.md]]：停用单控件透明导出层，正式收束到 atlas-first。
- [[decisions/015-将assets-json元数据收束到metadata分层.md]]：将 `assets` 下的 JSON 元数据统一迁入 `metadata/` 分层。
- [[decisions/016-引入可视化BBox微调工具.md]]：引入本地 BBox 可视化编辑器 `bbox_editor.py` 辅助 AI 识别管线。
- [[decisions/017-引入竖屏空间构图模型.md]]：针对竖屏 UI 建立纵向功能分层模型。
- [[decisions/018-将批量截图skill扩展为atlas主链.md]]：批量截图 Skill 正式覆盖控件裁切、复核与 atlas 图谱层。
- [[decisions/020-游戏ui-prompt-skill扩展为网页版ai交接包.md]]：`skills/06-game_ui_prompt_template.md` 新增 `web_ai_handoff_pack` 模式，支持把规范与 atlas 一起交给网页版 AI 使用。
- [[decisions/021-游戏ui-prompt-skill收束为规范联动与风格分支优先.md]]：`skills/06-game_ui_prompt_template.md` 改为精简版执行卡，强调与 `02` 联动并要求多风格系统先问偏好。
- [[decisions/022-游戏ui-prompt-skill改为依赖生成规范与通用风格分支.md]]：`skills/06-game_ui_prompt_template.md` 改为优先读取生成后的设计规范，并将风格选项从系统特例收束为通用提炼规则。
- [[decisions/023-游戏ui-prompt-skill补入手游热区尺寸与适配约束.md]]：`skills/06-game_ui_prompt_template.md` 新增手游热区、间距、安全区、画布与适配约束，并引入官方最小值。

Last updated: 2026-04-28
