---
type: source
title: "按钮 (Apple HIG)"
author: "Apple"
url: "https://developer.apple.com/cn/design/human-interface-guidelines/buttons"
date: 2026-04-13
format: [article]
key_points:
  - "多输入方式下，按钮必须提供足够的点击热区（通常44x44，visionOS 60x60）"
  - "交互反馈至关重要：按钮必须包含'按压/悬停'状态，否则用户会觉得无响应"
  - "在手柄或触控板环境下支持'弹性载入(Force Click)'等压感操作"
  - "不同状态需有视觉区分：空闲、悬停(Hover)、已选择、不可用"
game_focus: []
concepts_extracted:
  - wiki/concepts/按钮交互状态.md
  - wiki/concepts/最小触控热区.md
status: processed
---

## 核心要点总结

该指南定义了 iOS 及其他 Apple 平台的按钮设计标准，核心在于**交互的确定性**：

1. **触控与精度的平衡**：在小屏幕或手持设备上，通过规定最小热区（44pt）来降低玩家的操作负担。
2. **多态反馈**：强调了“状态”的重要性。游戏中的按钮也必须遵循逻辑：如果按下去没有视觉或触觉变化，玩家会因不确定操作是否生效而产生焦虑。
3. **适配能力**：支持多种输入设备（手柄、触控、压感）的统一交互体验。
