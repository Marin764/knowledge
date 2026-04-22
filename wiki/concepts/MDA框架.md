---
type: concept
title: "MDA 框架"
title_en: "MDA Framework"
aliases: [游戏设计框架]
created: 2026-04-21
updated: 2026-04-21
definition: "由 Robin Hunicke、Marc LeBlanc、Robert Tubbs 于 2004 年提出的游戏设计分析框架，将游戏分解为机制、动态、美学三个层面"
source_count: 2
sources:
  - wiki/source/GMTK-How-To-Think-Like-A-Game-Designer.md
  - wiki/source/GMTK-Protect-Players-From-Themselves.md
related_concepts:
  - wiki/concepts/设计愿景.md
tags: [game-design, framework, mechanics, aesthetics]
status: active
confidence: high
---

# MDA 框架

## 三个层面

| 层面 | 定义 | 在游戏中的位置 |
|------|------|----------------|
| **机制（Mechanics）** | 规则、系统、按钮功能、数值 | 代码层面 |
| **动态（Dynamic）** | 玩家对机制的反应和行为 | 玩家行动 |
| **美学（Aesthetics）** | 玩家的情感体验和感受 | 玩家情绪 |

## 应用方法

通过改变代码（机制），可以连锁影响玩家的行为（动态）和情感（美学）。

### 设计愿景
MDA 框架帮助设计者问出关键问题：
- 这个机制如何影响玩家行为？
- 这种行为如何影响玩家感受？
- 这种感受是否匹配游戏愿景？

## 相关案例

- **DOOM (2016)**："前冲战斗"愿景下，荣耀击杀机制激励激进打法
- **《花》**：移除升级、魔法、资源管理等不符合"放松"美学的机制
- **《异形：隔离》**：手动存档机制强化恐怖氛围