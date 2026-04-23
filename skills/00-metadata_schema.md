# Metadata Schema (Frontmatter 规范)

> **触发场景**：创建新页面或更新现有页面的 YAML 头信息时。

## 1. games/ (游戏实体)
```yaml
type: game
title: "游戏中文名"
title_en: "Game English Name"
created: YYYY-MM-DD
updated: YYYY-MM-DD
genre: [action, rpg]
platform: [PC, PS5]
sources: [raw/articles/xxx.md]
status: active
```

## 2. concepts/ (交互设计概念)
```yaml
type: concept
title: "概念名称"
aliases: [别名]
definition: "一句话定义"
game_referenced: [游戏名]
tags: [feedback, input]
status: active
```

## 3. mechanics/ (机制设计)
```yaml
type: mechanics
title: "机制名称"
category: [movement, combat, camera, ui, input]
game_examples: [例子]
implementation_notes: "技术实现要点"
status: active
```

## 4. source/ (来源摘要)
```yaml
type: source
title: "来源标题"
author: "作者名"
url: "原始链接"
format: [article, gdc, video, book]
key_points: ["要点1"]
```

## 5. ui_specs/ (UI 截图分析)
```yaml
type: ui_spec
game: "游戏名"
screen_type: [hud, menu]
source_image: "assets/xxx.jpg"
tags: [layout, alignment]
```
