# Game Interaction Design Wiki - Schema

> 这是整个知识库的"宪法"，定义了 AI 维护者的行为规范和工作流。

## 1. 目录结构规范

```
know/                          # 根目录
├── CLAUDE.md                 # 本文件 - Schema 定义
├── scripts/                  # 工具脚本
│   ├── lint.py               # 健康检查脚本（每次提交自动运行）
│   ├── generate_slides.py    # Marp 幻灯片生成器
│   └── wiki.sh               # 便捷命令入口
├── exports/                   # AI 生成的可交付物（幻灯片/图表）
├── wiki/
│   ├── index.md              # 知识库总索引（自动维护）
│   ├── log.md                # 操作日志（纯追加）
│   ├── games/                # 游戏实体页面 (e.g., 塞尔达传说-旷野之息.md)
│   ├── concepts/             # 交互设计概念 (e.g., hitstop.md, coyote-time.md)
│   ├── mechanics/            # 具体机制设计 (e.g., 锁定系统.md, 镜头跟随.md)
│   ├── source/               # 来源摘要 (每份原始资料一个)
│   └── comparisons/           # 跨游戏对比分析
├── raw/                      # 原始资料库（不可变，AI 只读）
│   ├── gdc_vault/            # GDC 演讲/总结
│   ├── articles/             # 博客文章
│   ├── game_manuals/        # 游戏设计文档
│   └── video_scripts/        # 视频文字稿
└── assets/                   # 图片/动图/GIF
```

## 2. Frontmatter 规范

每种 wiki 页面都有对应的 YAML frontmatter，格式如下：

### games/ (游戏实体)

```yaml
---
type: game
title: "游戏中文名"
title_en: "Game English Name"
created: 2026-04-13
updated: 2026-04-13
developer: ""
publisher: ""
release_date: ""
genre: [action, rpg, platformer]
platform: [PC, Switch, PS5]
source_count: 1
sources:
  - raw/articles/xxx.md
related_games:
  - wiki/games/塞尔达传说-旷野之息.md
related_concepts:
  - wiki/concepts/hitstop.md
tags: [combat, open-world, exploration]
status: active
confidence: medium
---
```

### concepts/ (交互设计概念)

```yaml
---
type: concept
title: "概念名称"
aliases: [别名1, 别名2]
created: 2026-04-13
updated: 2026-04-13
definition: "一句话定义这个概念"
game_referenced: [游戏名, 游戏名]
source_count: 2
sources:
  - raw/gdc_vault/xxx.md
  - raw/articles/xxx.md
related_concepts:
  - wiki/concepts/xxx.md
tags: [feedback, input, timing, animation]
status: active
confidence: high
---
```

### mechanics/ (机制设计)

```yaml
---
type: mechanics
title: "机制名称"
category: [movement, combat, camera, ui, input]
created: 2026-04-13
updated: 2026-04-13
description: "机制的详细描述"
game_examples: [例子]
implementation_notes: "技术实现要点"
source_count: 1
sources:
  - raw/video_scripts/xxx.md
related_mechanics:
  - wiki/mechanics/xxx.md
tags: []
status: active
---
```

### source/ (来源摘要)

```yaml
---
type: source
title: "来源标题"
author: "作者名"
url: "原始链接"
date: 2026-04-13
format: [article, gdc, video, book]
key_points:
  - "关键要点1"
  - "关键要点2"
game_focus: [游戏名]
concepts_extracted:
  - wiki/concepts/xxx.md
status: processed
---
```

## 3. 不可变性规则

- **raw/** 目录：只读。AI 不得修改、删除其中的任何文件。
- **assets/** 目录：只读。图片/GIF 仅供引用。
- **wiki/** 目录：AI 全权维护。创建、更新、删除均由 AI 执行。

## 4. 三大核心工作流

### 4.1 摄入 (Ingest)

**触发**：用户说 `ingest <file>` 或 `处理 <file>`

**完整流程**：
1. 读取原始文档 `raw/xxx`
2. 移动文件到正确分类（`articles/`、`game_manuals/`、`gdc_vault/`、`video_scripts/`）
3. 向用户确认 2-3 个核心要点（摘要 + 关键论断）
4. **完善 tags**：将导入插件生成的通用 `clippings` tag 替换为有意义的标签
   - 根据文档内容提取 2-4 个相关标签
   - 常用标签参考：`game-design`, `ui`, `input`, `feedback`, `platform`, `mobile`, `accessibility`, `typography`, `haptics`, `layout`, `adaptation`
5. 创建 `wiki/source/<source-name>.md`（来源摘要）
6. 更新或创建相关游戏页面 `wiki/games/`
7. 更新或创建相关概念页面 `wiki/concepts/`
8. 更新或创建相关机制页面 `wiki/mechanics/`
9. 检查新旧内容是否有矛盾，标记在页面中
10. 更新 `wiki/index.md`
11. 追加到 `wiki/log.md`
12. 向用户报告：创建/更新了哪些页面、有无矛盾

### 4.2 查询 (Query)

**触发**：用户提问（不以 ingest 开头）

**流程**：
1. 用户提出问题
2. AI 分析需要哪些 wiki 页面来回答
3. 读取相关页面（games/concepts/mechanics）
4. 综合信息，给出带引用的回答
5. **可选**：将回答回填到 wiki 作为新页面（如 comparison）

**格式**：回答可以是纯文本，也可以是：
- Markdown 页面
- 对比表格
- 包含 `---` 分页符的 Marp 幻灯片文件（当用户要求总结时可直接生成，存放在 `exports/` 目录）
- 图表代码

### 4.3 健康检查 (Lint)

**触发**：用户说 `lint` 或 `健康检查`

**检查项**：
- 页面间矛盾（concept 页的新结论是否推翻旧来源）
- 过时内容（数据/版本是否需要更新）
- 孤立页面（无入链的页面）
- Stub 页面（<100 字的占位符）
- 缺失页面（被引用但不存在的 wikilink）
- Frontmatter 不一致（必填字段缺失）
- 未摄入的 raw 文件

**输出**：报告 + 修复建议

## 5. 索引系统

### wiki/index.md 结构

```markdown
# Game Interaction Design Wiki

Last updated: 2026-04-13 | Pages: X | Sources: X

## Games (X)
- [[games/塞尔达传说-旷野之息]] — 开放世界动作冒险 (2 sources)
- [[games/空洞骑士]] — 2D 魂类平台跳跃 (3 sources)

## Concepts (X)
- [[concepts/hitstop]] — 打击停顿/顿帧 (4 sources)
- [[concepts/coyote-time]] — 土狼时间/跳跃宽容期 (3 sources)

## Mechanics (X)
- [[mechanics/锁定系统]] — 目标锁定机制 (2 sources)
- [[mechanics/镜头跟随]] — 相机跟随算法 (2 sources)

## Source Summaries (X)
- [[source/gdc-2023-action-design]] — GDC 2023 动作设计 (2026-04-02)
```

### wiki/log.md 结构

```markdown
## [2026-04-13] ingest | 游戏交互设计入门文章
- Source: raw/articles/intro-to-game-input.md
- Pages created: source/intro-to-game-input.md, concepts/input-delay.md
- Page updated: games/塞尔达传说-旷野之息.md
- Contradictions: none
```

## 6. 写作风格约定

- **文件名强制中文**：无论笔记内容是中文还是英文，所有 wiki/ 和 raw/ 文件名必须保存为中文
  - 正确：`游戏控制.md`、`触觉反馈.md`、`Core Haptics.md`
  - 错误：`game-controls.md`、`haptic-feedback.md`
  - 英文名称在 frontmatter 的 `title_en` 或 `aliases` 中标注
- **Wikilink**：使用 `[[wiki/games/xxx.md]]` 而非相对路径
- **引用格式**：每个论断必须注明来源 `[来源]`
- **中文优先**：游戏名/概念名用中文，英文名在 alias 或 title_en 中标注
- **动图引用**：用 `![描述](assets/xxx.gif)` 格式引用 GIF
- **代码块**：如果涉及技术实现，用 fenced code block 包裹

## 7. 特定领域约定

### 游戏交互设计的核心概念分类

1. **输入类 (Input)**：预输入、输入缓冲、输入延迟、取消动画
2. **反馈类 (Feedback)**：Hitstop顿帧、屏幕震动、音效反馈、视觉闪烁
3. **时机类 (Timing)**：土狼时间、跳跃缓冲、攻击前摇、闪避无敌帧
4. **物理类 (Physics)**：摩擦力、跳跃高度、重力曲线、碰撞盒
5. **相机类 (Camera)**：跟随算法、锁定视角、焦点转换、视野控制
6. **UI类 (UI)**：血条交互、血条闪烁时机、提示文字层级

### 交互手感评估维度

- **响应感**：输入到反馈的时间差
- **打击感**：攻击命中时的多感官反馈强度
- **节奏感**：动画节奏与玩家预期的匹配度
- **容错感**：系统对玩家失误的宽容程度
- **重量感**：角色移动/攻击时的惯性体验

## 8. 工具约定

### 8.1 脚本工具

| 脚本 | 用途 | 调用方式 |
|------|------|----------|
| `scripts/lint.js` | 健康检查：死链接、孤立页面、Frontmatter校验 | `node scripts/lint.js` |
| `scripts/generate_slides.js` | Marp幻灯片生成 | `node scripts/generate_slides.js --all` |
| `scripts/youtube.sh` | 抓取 YouTube 字幕并转为 Markdown | `bash scripts/youtube.sh <url> [标题]` |
| `scripts/wiki.sh` | 便捷命令入口 | `bash scripts/wiki.sh <command>` |

**Git Hooks**：`.git/hooks/pre-commit` 会在每次 `git commit` 时自动运行 `lint.py`，确保提交内容健康。

**搜索**：当 wiki 页面超过 100 个时，建议使用 qmd 搜索
- **可视化**：需要时用 Mermaid 画概念关系图
- **幻灯片**：需要输出演示时用 Marp 格式

---

*Schema version: 1.1 | Last updated: 2026-04-14*