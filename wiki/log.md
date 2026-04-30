# Wiki Operation Log

> 知识库操作记录，按时间顺序追加

## [2026-04-27] create | 剑与远征：启程 (AFK Journey) 精选资产提取与核心索引
- Source: `raw/screenshots/剑与远征：启程-GameUI.net/` (137 samples)
- Action: 从 137 张图中精选 12 张核心原型（招募、养成、商店、回归系统等），物理提取至 `assets/afk_journey_ui/` 并进行语义化命名；同步建立 `manifest-afk-core.json` 核心 Manifest。
- Files updated: MEMORY.md, wiki/analysis/剑与远征：启程-*.md, wiki/source/剑与远征：启程-全量截图索引清单.md
- Files created: `assets/afk_journey_ui/` (12 files), `assets/afk_journey_controls/metadata/screens/manifest-afk-core.json`
- Contradictions: none

## [2026-04-27] create | 引入可视化 BBox 微调工具
- Source: 解决人工复核时 JSON 坐标调整困难的问题
- Action: 新增 `scripts/images/bbox_editor.py`，提供基于 Python Tkinter 的本地可视化微调能力，支持拖拽和缩放 Bounding Box 并实时写回 JSON。同步增加 ADR 016。
- Files updated: MEMORY.md, decisions/INDEX.md
- Files created: `scripts/images/bbox_editor.py`, `decisions/016-引入可视化BBox微调工具.md`
- Contradictions: none

## [2026-04-27] create | 星穹铁道商店界面原型 V1
- Source: `assets/star_rail_ui/hsr-shop-main.jpg`, `assets/star_rail_ui/hsr-shop-world.jpg`, `assets/star_rail_controls/crops/*`
- Action: 新增 `exports/星穹铁道-商店界面原型_V1.html`，复用商店主界面与世界商店的页签、主面板、价格框、购买按钮、奖励面板与商品卡语义，生成一个固定 16:9 的可交互游戏内商店页面。
- Files updated: MEMORY.md, wiki/index.md
- Files created: `exports/星穹铁道-商店界面原型_V1.html`
- Contradictions: none

## [2026-04-13] init | Wiki initialized
- Action: Created directory structure and Schema
- Files created: CLAUDE.md, wiki/index.md, wiki/log.md## [2026-04-13] ingest | 浅谈2D动作游戏中的“顿帧” (Hitstop) 设计
- Source: raw/articles/test-hitstop.md
- Pages created: sources/test-hitstop.md, concepts/hitstop.md, games/空洞骑士.md, games/怪物猎人.md
- Contradictions: none

## [2026-04-27] update | 星铁剩余 18 张截图补齐 manifest 并并入 Atlas V3
- Source: `assets/star_rail_ui/` 剩余未落 manifest 的星铁系统截图
- Action: 为战斗 HUD、教程、活动、地图、消息、世界商店、模拟宇宙、光锥跃迁与单抽结果等页面新增 18 份 `manifest-*.json`，串行导出真实裁切图与复核图，并生成 `recognized-ui-elements-atlas-v3.png` 作为扩展后的全量图谱。
- Files updated: MEMORY.md, wiki/index.md, assets/目录结构说明.md, assets/star_rail_controls/目录结构说明.md
- Files created: `assets/star_rail_controls/manifest-*.json` (18 files), `assets/star_rail_controls/review/*`, `assets/star_rail_controls/crops/*`, `assets/star_rail_controls/atlas/manifest-recognized-ui-elements-atlas-v3.json`, `assets/star_rail_controls/atlas/recognized-ui-elements-atlas-v3.png`
- Contradictions: none

## [2026-04-27] update | 补齐旧批次 4 张角色养成页并完成 29 张星铁截图全量覆盖
- Source: `assets/star_rail_ui/hsr-char-attributes.jpg`, `assets/star_rail_ui/hsr-growth-lightcone.jpg`, `assets/star_rail_ui/hsr-growth-relic.jpg`, `assets/star_rail_ui/hsr-growth-relic-slots.jpg`
- Action: 为旧批次中只进入分析但未独立落 manifest 的 4 张页面补齐 `manifest-*.json`、真实裁切图与复核图，确保 `star_rail_ui/` 29 张截图全部进入标准化控件链路。
- Files updated: MEMORY.md, assets/star_rail_controls/atlas/manifest-recognized-ui-elements-atlas-v3.json
- Files created: `assets/star_rail_controls/manifest-char-attributes.json`, `assets/star_rail_controls/manifest-growth-lightcone.json`, `assets/star_rail_controls/manifest-growth-relic.json`, `assets/star_rail_controls/manifest-growth-relic-slots.json`
- Contradictions: none

## [2026-04-27] update | 停用单控件透明导出层并收束到 atlas-first
- Source: 用户明确不再需要单个透明控件资源层，资源目标转向 AI 可读图谱
- Action: 清理 `assets/star_rail_controls/generated/singles/`、移除 `scripts/images/extract_generated_controls.ps1` 与 `atlas/manifest-generated-ui-elements-atlas-v1.json`，新增 ADR 014，明确 `generated/` 仅保留为历史实验归档。
- Files updated: MEMORY.md, decisions/INDEX.md, assets/目录结构说明.md, assets/star_rail_controls/目录结构说明.md
- Files created: `decisions/014-停用-ai-单控件透明层并收束到atlas主产物.md`
- Files deleted: `assets/star_rail_controls/generated/singles/`, `scripts/images/extract_generated_controls.ps1`, `assets/star_rail_controls/atlas/manifest-generated-ui-elements-atlas-v1.json`
- Contradictions: none

## [2026-04-27] update | 将 assets JSON 元数据收束到 metadata 分层
- Source: 用户要求清理 `assets/` 下零散 JSON，让目录更干净
- Action: 在 `assets/star_rail_controls/` 下新增 `metadata/screens`、`metadata/atlas`、`metadata/generated`，并将截图 manifest、atlas manifest、重建日志与候选队列全部迁入对应子目录；同步更新目录说明、MEMORY 与 ADR 索引。
- Files updated: MEMORY.md, decisions/INDEX.md, assets/目录结构说明.md, assets/star_rail_controls/目录结构说明.md
- Files created: `assets/star_rail_controls/metadata/`, `decisions/015-将assets-json元数据收束到metadata分层.md`
- Files moved: `assets/star_rail_controls/*.json` -> `assets/star_rail_controls/metadata/screens|generated`, `assets/star_rail_controls/atlas/*.json` -> `assets/star_rail_controls/metadata/atlas`, `assets/star_rail_controls/generated/*.json` -> `assets/star_rail_controls/metadata/generated`
- Contradictions: none
## [2026-04-13] ingest | 【游戏交互】手游适配设计
- Source: raw/articles/【游戏交互】手游适配设计.md
- Pages created: sources/【游戏交互】手游适配设计.md, concepts/UI锚点.md, concepts/安全区域适配.md, games/哈利波特.md, games/炉石传说.md, games/天谕.md
- Contradictions: none

## [2026-04-13] ingest | The Rise of Cross-Platform Play
- Source: raw/articles/跨平台联机的崛起.md
- Pages created: sources/The-Rise-of-Cross-Platform-Play.md, concepts/跨平台联机.md, concepts/跨端输入平衡.md, games/堡垒之夜.md, games/使命召唤：战区.md, games/火箭联盟.md, games/我的世界.md
- Contradictions: none
## [2026-04-13] ingest | Apple HIG 游戏设计与UI规范 (3篇)
- Source: Clippings/小屏幕游戏界面适配.md, Clippings/按钮.md, Clippings/针对游戏设计.md
- Pages created: sources/adapting-game-interface-smaller-screens.md, sources/apple-hig-buttons.md, sources/designing-for-games.md, concepts/最小触控热区.md, concepts/按钮交互状态.md, concepts/触觉反馈.md, concepts/多输入方式适配.md, concepts/动态UI适配.md
- Contradictions: none
## [2026-04-15] ingest | 沉浸式交互让游戏更加迷人 - 腾讯游戏学堂
- Source: raw/articles/沉浸式交互让游戏更加迷人.md
- Pages created: sources/沉浸式交互让游戏更加迷人.md, concepts/拟物化交互.md, concepts/潜意识交互.md, concepts/沉浸式反馈.md, concepts/子弹时间.md, games/Metro归来.md
- Pages updated: wiki/index.md
- Contradictions: none

## [2026-04-21] ingest | Battle Passes - Everything You Ought to Know
- Source: raw/articles/Battle Passes Analysis.md
- Pages created: source/战斗通行证深度分析.md, mechanics/战斗通行证系统.md, games/皇室战争.md, games/部落冲突.md
- Pages updated: games/堡垒之夜.md, wiki/index.md
- Contradictions: none

## [2026-04-21] ingest | Brawl Stars Ditched Loot Boxes
- Source: raw/articles/Brawl Stars Loot Box Removal.md
- Pages created: source/Brawl Stars放弃战利品箱分析.md, mechanics/战利品箱.md, games/荒野乱斗.md
- Pages updated: wiki/index.md
- Contradictions: none

## [2026-04-21] ingest | Daily Missions in Puzzles
- Source: raw/articles/Daily Missions in Puzzles.md
- Pages created: source/每日任务设计分析.md, mechanics/每日任务系统.md, concepts/约定机制.md, games/皇家对决.md, games/Time Blast.md
- Pages updated: wiki/index.md
- Contradictions: none

## [2026-04-21] ingest | Seven Things the 2025 State of Gaming Report Actually Tells Us
- Source: Clippings/Seven Things the 2025 State of Gaming Report Actually Tells Us.md
- Pages created: source/2025-State-of-Gaming-Report.md, concepts/市场集中化.md, concepts/独立友群游戏.md, concepts/买量驱动型设计.md, concepts/Web商店变现.md
- Pages updated: Clippings/Seven Things the 2025 State of Gaming Report Actually Tells Us.md (tags), wiki/index.md
- Contradictions: none

## [2026-04-21] update | UI Analysis Spec Upgrade & Full OCR Backfill
- Source: All 44 processed screenshots in `raw/screenshots/ready/`
- Action: Updated `skills/01-ui_analysis.md` with OCR mandatory workflow; Backfilled OCR Context for 12 files in `wiki/analysis/`.
- Pages updated: wiki/analysis/无期迷途-*.md, wiki/analysis/星穹铁道-*.md, wiki/analysis/王者荣耀-*.md, wiki/analysis/逆水寒-*.md
- Contradictions: none

## [2026-04-21] ingest | Focus Friend Retention Analysis
- Source: raw/articles/Focus Friend Retention Analysis.md
- Pages created: source/Focus Friend留存机制分析.md, mechanics/建设与个性化留存.md, concepts/心血辩护效应.md, games/卡通农场.md
- Pages updated: wiki/index.md
- Contradictions: none

## [2026-04-23] update | 交互规范 Skill 重构为 AI 生成合同
- Source: skills/01-ui_analysis.md, skills/02-game_system_ux_spec.md
- Action: 将交互规范主模板改为页面地图、区域合同、组件合同、状态/导航矩阵和 UI Manifest；同步强化 ui_analysis 的页面矩阵、区域拆解和组件清单输出。
- Files updated: skills/01-ui_analysis.md, skills/02-game_system_ux_spec.md, MEMORY.md, decisions/INDEX.md
- Files created: decisions/004-交互规范转向生成合同.md
- Contradictions: none

## [2026-04-23] update | 四款回归系统按新结构回填
- Source: wiki/analysis/无期迷途-回归系统.md, wiki/analysis/星穹铁道-回归系统.md, wiki/analysis/王者荣耀-回归系统.md, wiki/analysis/逆水寒-回归系统.md
- Action: 将四篇回归系统分析页回填为页面矩阵、区域拆解、组件清单、导航线索和 Analysis Manifest；基于四篇分析生成 `exports/回归系统-交互设计规范_V2.md`。
- Files updated: wiki/analysis/无期迷途-回归系统.md, wiki/analysis/星穹铁道-回归系统.md, wiki/analysis/王者荣耀-回归系统.md, wiki/analysis/逆水寒-回归系统.md, wiki/index.md, MEMORY.md
- Files created: exports/回归系统-交互设计规范_V2.md
- Contradictions: none

## [2026-04-23] create | 回归系统网页原型
- Source: exports/回归系统-交互设计规范_V2.md
- Action: 新增 `exports/回归系统-网页原型.html`，将回归系统规范转译为网页原生展示方案，明确避免手游式滑动轨道、强弹窗链和场景入口复刻。
- Files updated: wiki/index.md, MEMORY.md, decisions/INDEX.md
- Files created: exports/回归系统-网页原型.html, decisions/005-回归系统网页原型采用网页原生交互.md
- Contradictions: none

## [2026-04-23] update | 回归系统 HTML 原型改为 16:9 游戏界面稿
- Source: exports/回归系统-交互设计规范_V2.md
- Action: 删除网页专题式原型 `exports/回归系统-网页原型.html`，新增 `exports/回归系统-界面原型_V1.html`，改为 16:9 比例的游戏界面 HTML 稿。
- Files updated: wiki/index.md, MEMORY.md, decisions/INDEX.md
- Files created: exports/回归系统-界面原型_V1.html, decisions/006-回归系统-html-原型改为16比9游戏界面稿.md
- Files removed: exports/回归系统-网页原型.html
- Contradictions: none

## [2026-04-24] create | 游戏 UI 生成提示模板 Skill
- Source: 对“为什么直接生成会偏网页风格”的讨论结论
- Action: 新增 `skills/06-game_ui_prompt_template.md`，沉淀游戏 UI Prompt 骨架、反网页化词库、16:9 默认构图和按 HTML/Figma/图片分媒介模板；同步接入路由层。
- Files updated: AGENTS.md, CLAUDE.md, rules.md, MEMORY.md, decisions/INDEX.md
- Files created: skills/06-game_ui_prompt_template.md, decisions/007-将游戏-ui-生成-prompt-模板独立为-skill.md
- Contradictions: none

## [2026-04-24] create | 回归系统 16:9 线框原型
- Source: exports/回归系统-交互设计规范_V2.md, skills/06-game_ui_prompt_template.md
- Action: 新增 `exports/回归系统-界面线框原型_V2.html`，采用灰白低保真线框形式，优先验证回归系统主界面的布局规范、信息结构、状态分区和模块层级，不直接生成高保真视觉。
- Files updated: wiki/index.md, MEMORY.md
- Files created: exports/回归系统-界面线框原型_V2.html
- Contradictions: none

## [2026-04-24] update | 回归系统线框稿重构为多页面可交互原型
- Source: exports/回归系统-交互设计规范_V2.md
- Action: 将 `exports/回归系统-界面线框原型_V2.html` 重构为严格对照规范的多页面交互线框稿，补齐 `page.welcome / page.hub / page.progress / page.signin / page.catchup / page.high_value_reward / page.content_guidance`，并实现从 Hub 到各子页、从欢迎弹窗进入 Hub、以及从详情页返回 Hub 的基础跳转。
- Files updated: exports/回归系统-界面线框原型_V2.html, wiki/index.md, MEMORY.md
- Contradictions: none

## [2026-04-24] fix | 回归系统线框稿页面叠层与点击修复
- Source: 用户反馈“无法点击交互，而且所有界面叠在一起”
- Action: 修复 `exports/回归系统-界面线框原型_V2.html` 的初始激活状态与交互逻辑，改为一次只显示一个页面；欢迎页单独显示，进入后再切换到 Hub，并补充按钮显式交互样式。
- Files updated: exports/回归系统-界面线框原型_V2.html, MEMORY.md
- Contradictions: none

## [2026-04-24] update | 游戏 UI Skill 升级为线框原型优先
- Source: 用户要求严格按规范生成灰白线框、可交互、无网页化噪音的游戏界面原型
- Action: 重写 `skills/02-game_system_ux_spec.md` 与 `skills/06-game_ui_prompt_template.md`，新增 `wireframe_interactive` / `wireframe_interactive_html` 模式，补齐页面互斥显示、默认页、交互原型合同、占位符规则、元信息隐藏和线框表现红线。
- Files updated: skills/02-game_system_ux_spec.md, skills/06-game_ui_prompt_template.md, MEMORY.md, decisions/INDEX.md
- Files created: decisions/009-游戏-ui-skill-升级为线框原型优先.md
- Contradictions: none

## [2026-04-24] update | 回归系统线框稿按新 Skill 重做
- Source: `skills/02-game_system_ux_spec.md`, `skills/06-game_ui_prompt_template.md`, `exports/回归系统-交互设计规范_V2.md`
- Action: 重写 `exports/回归系统-界面线框原型_V2.html`，按新的线框原型模式移除界面中的规范标签、说明条和网页化噪音，改为左侧页签切换、单页显示、游戏内容占位和纯灰白线框结构。
- Files updated: exports/回归系统-界面线框原型_V2.html, MEMORY.md
- Contradictions: none

## [2026-04-24] create | 星铁商店 UI 控件裁切 MVP
- Source: `assets/star_rail_ui/hsr-shop-main.jpg`
- Action: 新增 `scripts/images/extract_ui_crops.ps1` 与 `assets/star_rail_controls/manifest-shop-main.json`，基于手动 bbox 标注导出 16 个控件裁切图，并生成带框复核图 `hsr-shop-main-v1-annotated.png` 与总览图 `hsr-shop-main-v1-contact-sheet.png`。
- Files updated: wiki/index.md, MEMORY.md, decisions/INDEX.md
- Files created: assets/star_rail_controls/manifest-shop-main.json, assets/star_rail_controls/crops/*, assets/star_rail_controls/review/*, scripts/images/extract_ui_crops.ps1, decisions/010-引入-ui-控件裁切试验管线.md
- Contradictions: none

## [2026-04-24] update | 星铁控件裁切扩展到主菜单与合成界面
- Source: `assets/star_rail_ui/hsr-hub-phone-menu.jpg`, `assets/star_rail_ui/hsr-system-synthesis.jpg`
- Action: 新增 `manifest-hub-phone-menu.json`、`manifest-system-synthesis.json` 与 `rebuild-queue-v1.json`，继续导出两张截图的控件裁切图、复核图和 contact sheet，累计形成 47 个控件裁切资源，并整理首批适合图生图重建的候选控件。
- Files updated: MEMORY.md
- Files created: assets/star_rail_controls/manifest-hub-phone-menu.json, assets/star_rail_controls/manifest-system-synthesis.json, assets/star_rail_controls/rebuild-queue-v1.json, assets/star_rail_controls/review/hsr-hub-phone-menu-v1-*.png, assets/star_rail_controls/review/hsr-system-synthesis-v1-*.png, assets/star_rail_controls/crops/*
- Contradictions: none

## [2026-04-24] create | 星铁 AI 控件重建试验首图
- Source: `assets/star_rail_controls/rebuild-queue-v1.json` 与外部生成图目录
- Action: 新增 `assets/star_rail_controls/generated/rebuild-log-v1.json`，并将首张 AI 控件重建图保存为 `assets/star_rail_controls/generated/star-rail-controls-rebuild-sheet-v1.png`，同时新增 ADR 011 说明 AI 重建产物目录的职责边界。
- Files updated: MEMORY.md, decisions/INDEX.md
- Files created: assets/star_rail_controls/generated/star-rail-controls-rebuild-sheet-v1.png, assets/star_rail_controls/generated/rebuild-log-v1.json, decisions/011-引入-ai-控件重建试验产物目录.md
- Contradictions: none

## [2026-04-24] update | 星铁 AI 底板与框体重建试验第二图
- Source: 首批星铁截图裁切结果与第二张外部生成图
- Action: 将第二张 AI 重建图保存为 `assets/star_rail_controls/generated/star-rail-backplates-rebuild-sheet-v1.png`，并在 `rebuild-log-v1.json` 中补充 `category / content_type / controls / based_on` 标注，明确其为底板与框体重建设计参考。
- Files updated: assets/star_rail_controls/generated/rebuild-log-v1.json, MEMORY.md
- Files created: assets/star_rail_controls/generated/star-rail-backplates-rebuild-sheet-v1.png
- Contradictions: none

## [2026-04-24] update | 星铁 AI 重建拼板拆分为单控件透明资源
- Source: `assets/star_rail_controls/generated/star-rail-controls-rebuild-sheet-v1.png`, `assets/star_rail_controls/generated/star-rail-backplates-rebuild-sheet-v1.png`
- Action: 新增 `scripts/images/extract_generated_controls.ps1`，基于两份拼板 manifest 批量导出 10 个透明 PNG 单控件，按分类写入 `assets/star_rail_controls/generated/singles/`，并创建 `manifest-generated-singles-v1.json` 作为单控件层索引，同时新增 ADR 012 记录该导出层的职责边界。
- Files updated: MEMORY.md, decisions/INDEX.md, assets/star_rail_controls/generated/rebuild-log-v1.json
- Files created: scripts/images/extract_generated_controls.ps1, assets/star_rail_controls/generated/singles/*, assets/star_rail_controls/generated/singles/manifest-generated-singles-v1.json, decisions/012-引入-ai-单控件透明导出目录.md
- Contradictions: none

## [2026-04-24] update | assets 目录结构补充说明并澄清控件资源分层
- Source: `assets/`, `assets/star_rail_controls/`
- Action: 新增 `assets/目录结构说明.md` 与 `assets/star_rail_controls/目录结构说明.md`，明确 `genshin_ui / star_rail_ui / star_rail_controls` 三个顶层目录的职责边界，并将星铁控件资源进一步拆解为真实裁切、复核、AI 重建和单控件透明导出四层语义。
- Files updated: MEMORY.md
- Files created: assets/目录结构说明.md, assets/star_rail_controls/目录结构说明.md
- Contradictions: none

## [2026-04-24] update | 复杂底板资源停止强制透明导出
- Source: `assets/star_rail_controls/generated/manifest-backplates-rebuild-sheet-v1.json`, `scripts/images/extract_generated_controls.ps1`
- Action: 将单控件导出脚本扩展为支持 `output_mode`，并将 `backplate / info_panel / dialog` 类资产切换为矩形导出，避免复杂框体在自动透明化时出现脏边、吃边和发硬边缘；规则控件仍可继续使用透明模式。
- Files updated: MEMORY.md, scripts/images/extract_generated_controls.ps1, assets/star_rail_controls/generated/manifest-backplates-rebuild-sheet-v1.json
- Files created: none
- Contradictions: none

## [2026-04-24] update | 建立星铁 UI Atlas 图谱层并整合已生成元素
- Source: `assets/star_rail_controls/generated/singles/`, `assets/star_rail_controls/crops/`
- Action: 新增 `scripts/images/build_control_atlas.ps1` 与 `assets/star_rail_controls/atlas/`，产出 `generated-ui-elements-atlas-v1.png` 用于整合已生成 UI 元素，并产出 `recognized-ui-elements-atlas-v1.png` 作为已识别其他元素的补充图谱，同时新增 ADR 013 明确 atlas 为面向 AI 使用的主参考层。
- Files updated: MEMORY.md, decisions/INDEX.md, assets/目录结构说明.md, assets/star_rail_controls/目录结构说明.md
- Files created: scripts/images/build_control_atlas.ps1, assets/star_rail_controls/atlas/manifest-generated-ui-elements-atlas-v1.json, assets/star_rail_controls/atlas/manifest-recognized-ui-elements-atlas-v1.json, assets/star_rail_controls/atlas/generated-ui-elements-atlas-v1.png, assets/star_rail_controls/atlas/recognized-ui-elements-atlas-v1.png, decisions/013-引入-ui-atlas-图谱层.md
- Contradictions: none

## [2026-04-24] update | Atlas 扩展到遗器详情、支援、跃迁与任务日志
- Source: `assets/star_rail_ui/hsr-growth-relic-detail.jpg`, `assets/star_rail_ui/hsr-system-friend-support.jpg`, `assets/star_rail_ui/hsr-wish-stellar-warp.jpg`, `assets/star_rail_ui/hsr-system-mission-log.jpg`
- Action: 新增 4 份截图 manifest，累计导出 34 个新控件与对应复核图，并基于更完整的代表性元素重建 `recognized-ui-elements-atlas-v2.png`，将星铁 UI 图谱覆盖面扩展到遗器详情、支援列表、跃迁与任务日志页面。
- Files updated: MEMORY.md, wiki/index.md, assets/star_rail_controls/目录结构说明.md
- Files created: assets/star_rail_controls/manifest-growth-relic-detail.json, assets/star_rail_controls/manifest-system-friend-support.json, assets/star_rail_controls/manifest-wish-stellar-warp.json, assets/star_rail_controls/manifest-system-mission-log.json, assets/star_rail_controls/atlas/manifest-recognized-ui-elements-atlas-v2.json, assets/star_rail_controls/atlas/recognized-ui-elements-atlas-v2.png, assets/star_rail_controls/review/hsr-*-v1-annotated.png, assets/star_rail_controls/review/hsr-*-v1-contact-sheet.png, assets/star_rail_controls/crops/*
- Contradictions: none

## [2026-04-24] update | 扩展识别范围到角色养成主界面并整理进 Atlas V2
- Source: `assets/star_rail_ui/hsr-char-attributes.jpg`, `assets/star_rail_ui/hsr-growth-lightcone.jpg`, `assets/star_rail_ui/hsr-growth-relic.jpg`, `assets/star_rail_ui/hsr-growth-relic-slots.jpg`
- Action: 读取并筛选角色属性、光锥主界面、遗器主界面和遗器槽位页中的高价值元素，将其代表性控件加入 `recognized-ui-elements-atlas-v2` 的策展范围，使图谱从“局部功能页”扩展到“角色养成核心页面”。
- Files updated: MEMORY.md, assets/star_rail_controls/atlas/manifest-recognized-ui-elements-atlas-v2.json
- Files created: none
- Contradictions: none

## [2026-04-27] update | 为新 AI 补充星铁界面生成入口说明
- Source: `assets/star_rail_controls/atlas/recognized-ui-elements-atlas-v3.png`, `assets/star_rail_controls/metadata/atlas/manifest-recognized-ui-elements-atlas-v3.json`, `assets/star_rail_controls/metadata/screens/`
- Action: 新增 [assets/给新AI的星铁界面生成说明.md](星铁界面生成说明.md)，将 `atlas v3 -> atlas manifest -> screen manifest -> crops -> 原图` 固化为推荐阅读顺序，并明确这套资产更适合生成哪些星铁风格界面、哪些方向不适合直接做。
- Files updated: MEMORY.md, assets/目录结构说明.md
- Files created: assets/给新AI的星铁界面生成说明.md
- Contradictions: none

## [2026-04-27] update | 修复 assets 入口死链并补齐批量截图 atlas 主链
- Source: `assets/目录结构说明.md`, `skills/03-batch_image_ingest.md`
- Action: 修复 `assets/目录结构说明.md` 中指向“给新 AI 的星铁界面生成说明”的死链；将 `skills/03-batch_image_ingest.md` 从“原型图确权即结束”的旧版流程扩展为“两段式主链”，正式纳入 `metadata/screens -> crops/review -> metadata/atlas -> atlas`。
- Files updated: MEMORY.md, decisions/INDEX.md
- Files created: decisions/018-将批量截图skill扩展为atlas主链.md
- Contradictions: none

## [2026-04-27] update | 按新版 Skill 01/02 重做四个战令案例与战令规范 V4
- Source: `raw/screenshots/ready/无期迷途-战令-*`, `raw/screenshots/ready/星穹铁道-战令-*`, `raw/screenshots/ready/王者荣耀-战令-*`, `raw/screenshots/ready/逆水寒战令-*`
- Action: 基于四组战令截图重新分析无期迷途、星穹铁道、王者荣耀、逆水寒战令系统，四篇 `wiki/analysis/*战令系统.md` 全部改为“页面矩阵 -> 空间区域 -> 组件状态 -> 跳转关系 -> Analysis Manifest”的新版结构；同时新建 [exports/战令系统-交互设计规范_V4.md](../exports/战令系统-交互设计规范_V4.md)，将战令总规范改写为页面合同式主文档，并将索引切换到 V4。
- Files updated: MEMORY.md, wiki/index.md
- Files created: exports/战令系统-交互设计规范_V4.md
- Contradictions: 逆水寒 `琳琅商店` 与无期迷途 `奖励预览` 的独立页面未在当前截图集中展开，正文已标注 `⚠️ 待裁定`

## [2026-04-28] update | 合并回归系统规范 V2/V3 为单一主入口 V4 并删除 V1
- Source: `exports/回归系统-交互设计规范_V2.md`, `exports/回归系统-交互设计规范_V3.md`
- Action: 新建 [exports/回归系统-交互设计规范_V4.md](../exports/回归系统-交互设计规范_V4.md)，合并 V2 的完整页面合同、状态矩阵、UI Manifest 与 V3 的 Spatial Slot、视觉空间蓝图、防网页化约束；同步将 `V2/V3` 标记为 `superseded`，删除 `exports/回归系统-交互设计规范_V1.md`，并将 [wiki/index.md](index.md) 的回归系统入口切换到 V4。
- Files updated: MEMORY.md, wiki/index.md, exports/回归系统-交互设计规范_V2.md, exports/回归系统-交互设计规范_V3.md
- Files created: exports/回归系统-交互设计规范_V4.md
- Files deleted: exports/回归系统-交互设计规范_V1.md
- Contradictions: none

## [2026-04-28] update | 扩展游戏 UI Prompt Skill 为网页版 AI 交接包模式
- Source: `skills/06-game_ui_prompt_template.md`
- Action: 为游戏 UI Prompt Skill 新增 `web_ai_handoff_pack` 模式，补入附件清单、阅读顺序、规范摘要、atlas 使用规则与网页版 AI 自包含交接模板，使其既能供本地 agent 使用，也能把交互规范与 UI 图谱一起打包给网页版 AI 生图。
- Files updated: MEMORY.md, decisions/INDEX.md, skills/06-game_ui_prompt_template.md
- Files created: decisions/020-游戏ui-prompt-skill扩展为网页版ai交接包.md
- Contradictions: none

## [2026-04-28] update | 收束游戏 UI Prompt Skill 为规范联动与风格偏好优先
- Source: `skills/06-game_ui_prompt_template.md`, `skills/02-game_system_ux_spec.md`
- Action: 将游戏 UI Prompt Skill 重写为更精简的执行卡，明确它必须先读取设计规范 Skill 的产出，再转译为 Prompt；同时把“多风格系统先确认用户偏好”写成硬规则，并为回归系统沉淀了“内容总览型 / 进度清晰型 / 奖励强化型”三种风格分支。
- Files updated: MEMORY.md, decisions/INDEX.md, skills/06-game_ui_prompt_template.md
- Files created: decisions/021-游戏ui-prompt-skill收束为规范联动与风格分支优先.md
- Contradictions: none

## [2026-04-28] update | 调整游戏 UI Prompt Skill 为依赖生成规范与通用风格分支
- Source: `skills/06-game_ui_prompt_template.md`
- Action: 将 Skill 的依赖对象从“设计规范 Skill”明确收束为“生成后的设计规范文档”；将比例描述改为默认 `16:9`、横屏优先但不强制锁死方向；删除不必要的默认输入材料描述；并把回归系统的固定风格选项改为通用风格分支提炼规则。
- Files updated: MEMORY.md, decisions/INDEX.md, skills/06-game_ui_prompt_template.md
- Files created: decisions/022-游戏ui-prompt-skill改为依赖生成规范与通用风格分支.md
- Contradictions: none

## [2026-04-29] update | 为游戏 UI Prompt Skill 补入手游热区与基础适配约束
- Source: `skills/06-game_ui_prompt_template.md`
- Action: 基于 Apple、Android 和 WCAG 官方资料，为 Skill 新增最小触控热区、相邻可点击目标最小间距、安全区/手势区避让、默认画布尺寸和基础横竖屏适配约束，并将这组约束纳入 Prompt 执行协议。
- Files updated: MEMORY.md, decisions/INDEX.md, skills/06-game_ui_prompt_template.md
- Files created: decisions/023-游戏ui-prompt-skill补入手游热区尺寸与适配约束.md
- Contradictions: none

## [2026-04-29] update | 生成回归系统生图特化规范 V5
- Source: `exports/回归系统-交互设计规范_V4.md`
- Action: 复制并改写为 [exports/回归系统-交互设计规范_V5.md](../exports/回归系统-交互设计规范_V5.md)，将规范目标聚焦到“上传资料后单页生图”，强调回归系统是整套系统，但每次只允许生成其中一个页面；新增页面选择规则、风格分支、必须出现/禁止出现表和单页生图 Prompt 模板；同步将 [wiki/index.md](index.md) 的回归系统主入口切换到 V5，并将 `V4` 标记为 `superseded`。
- Files updated: MEMORY.md, wiki/index.md, exports/回归系统-交互设计规范_V4.md
- Files created: exports/回归系统-交互设计规范_V5.md
- Contradictions: none

## [2026-04-30] update | 整理三国杀 UI 组件为 AI 生图参考包
- Source: `assets/three_kingdoms_kill_controls/official_components/`, `assets/three_kingdoms_kill_ui/`
- Action: 保留 `official_components/` 作为来源区，新增 `components/` 和 `patterns/` 两层英文命名参考图；将按钮、Tab、弹窗、状态角标、对勾图标归入组件层，将战斗 HUD、抽卡、通用系统页、活动页、武将皮肤页归入组合模式层；新增组件语义清单、组合模式语义清单和给新 AI 的三国杀界面生成说明，明确 agent 读取顺序与生图用法。
- Files updated: MEMORY.md, decisions/INDEX.md, assets/目录结构说明.md
- Files created: assets/三国杀界面生成说明.md, assets/three_kingdoms_kill_controls/目录结构说明.md, assets/three_kingdoms_kill_controls/metadata/components/sgs-components-for-ai.json, assets/three_kingdoms_kill_controls/metadata/patterns/sgs-patterns-for-ai.json, decisions/024-三国杀ui资源拆分为组件与组合模式参考包.md
- Contradictions: none

## [2026-04-30] update | 三国杀新增透明组件组切图并更新组件语义
- Source: `assets/three_kingdoms_kill_controls/official_components/武将 势力.png`, `武将 阶框.png`, `兵种图标.png`, `武将卡面.png`
- Action: 将新增透明底组件组拆分为面向 AI 读取的英文命名组件：`components/faction/` 5 个势力竖条、`components/hero-frame/` 5 个武将阶框、`components/troop/` 23 个兵种图标、`components/hero-card/` 10 张武将卡面；生成 `components/sgs-new-components-contact-sheet-v1.png` 作为新增组件复核总览，并同步补充组件语义、来源清单和目录说明。
- Files updated: MEMORY.md, assets/三国杀界面生成说明.md, assets/three_kingdoms_kill_controls/目录结构说明.md, assets/three_kingdoms_kill_controls/metadata/components/sgs-components-for-ai.json, assets/three_kingdoms_kill_controls/metadata/components/sgs-official-components.json
- Files created: assets/three_kingdoms_kill_controls/components/faction/*.png, assets/three_kingdoms_kill_controls/components/hero-frame/*.png, assets/three_kingdoms_kill_controls/components/troop/*.png, assets/three_kingdoms_kill_controls/components/hero-card/*.png, assets/three_kingdoms_kill_controls/components/sgs-new-components-contact-sheet-v1.png
- Contradictions: none

## [2026-04-30] create | 回归系统三国杀 HUD 界面原型 V1
- Source: `exports/回归系统-交互设计规范_V5.md`, `assets/three_kingdoms_kill_controls/metadata/components/sgs-components-for-ai.json`, `assets/three_kingdoms_kill_controls/components/`, `assets/three_kingdoms_kill_controls/patterns/event/sgs-pattern-event-layout.png`
- Action: 新增 `exports/回归系统-三国杀HUD界面原型_V1.html`，按 `page.hub` 单页合同生成 16:9 横屏游戏 HUD 原型；界面采用左侧竖向 Tab、中央回归主舞台、入口矩阵、右侧高价值奖励和底部主操作区，直接引用三国杀 modal 大框、活动 pattern、武将卡面、势力竖条、阶框、兵种图标、对勾与按钮状态合集。
- Files updated: MEMORY.md
- Files created: exports/回归系统-三国杀HUD界面原型_V1.html
- Contradictions: none

## [2026-04-30] update | 忽略 assets 并从 Git 索引移除已跟踪视觉资产
- Source: `.gitignore`, `assets/`
- Action: 将 `assets/` 加入 `.gitignore`，并将已被 Git 跟踪的 `assets/genshin_ui/` 图片从索引中移除但保留本地文件；后续 GitHub 默认只同步知识库文本、规范、脚本和元规则，标准化视觉资产留在本地工作区。
- Files updated: .gitignore, MEMORY.md, decisions/INDEX.md
- Files created: decisions/025-忽略assets并停止上传标准化视觉资产.md
- Contradictions: none
