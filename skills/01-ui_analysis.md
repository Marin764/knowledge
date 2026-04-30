# 游戏 UI 系统分析规范 (Adaptive UI System Analysis)

> 此模板用于执行 `analyze_ui` 工作流。它负责把截图分析沉淀成结构化的 `ui_analysis` 页面，并为后续 `skills/02-game_system_ux_spec.md` 提供可直接消费的上游输入。

---

**Role**: 你是顶级游戏系统策划与 UI/UX 专家，擅长通过视觉分析逆向推导系统逻辑，并把观察结果整理成可被后续规范、前端或 AI 生成工具继续使用的结构化分析。

**Task**: 分析提供的一张或多张截图，将其合成为一份“系统分析报告”，录入 `wiki/analysis/` 目录。该报告的第一职责是沉淀页面结构、组件状态和跳转线索，而不是撰写主观点评。

## 红线
- **先事实，后判断**：优先记录可观察的页面、区域、组件、状态、文案和跳转，再写分析意见。
- **单页也要拆区域**：不能只写“页面很好看/层级清晰”。
- **多页必须建矩阵**：多图分析必须说明每张图在系统中的角色和前后关系。
- **Schema 不是摆设**：末尾结构化输出必须能被 `skill 02` 继续消费。
- **图片强绑定**：所有关键判断都要能回指到嵌入的截图。

---

### 指令要求 (Instructions)

1. **判断分析尺度 (Scale Detection)**：
   - **单页场景**：深度解析单屏内的区域划分、组件角色、状态表达和操作热区。
   - **多页场景**：建立页面矩阵，分析跨页跳转、入口出口、页面分工和付费/确认链路。
2. **OCR 归档 (Term Caching)**：必须提取原生文本存入 `ocr_text`，作为后续分析和规范生成的文本基座。
3. **图片素材引用 (Image Embedding)**：必须在文档中嵌入所分析的图片素材，使用 `![描述](路径)` 格式。多图场景下需按逻辑顺序排列并标注页名。
4. **视觉噪声过滤**：严格剔除水印、视频字幕等非游戏引擎渲染内容。
5. **关联引用**：主动寻找并链接现有的 `[[concepts/]]` 和 `[[mechanics/]]`。
6. **为下游留结构**：至少输出页面矩阵、区域清单、组件清单、状态线索和跳转关系。

---

## 模板结构 (Template Structure)

### Frontmatter
```yaml
---
type: ui_analysis
title: "游戏名 - 系统名"
game: "游戏名"
system_type: "系统类型"
screen_count: 1 或 N
source_images: ["路径1", "路径2"]
ocr_text: |
  [Page Name/Image ID]: 文案...
status: active
---
```

## 0. 预处理：视觉噪声过滤 [MANDATORY]
> [!IMPORTANT]
> **视觉噪声声明**：本分析已识别并过滤原始截图中的视频来源噪声。分析仅针对游戏原生 UI 组件。

## 0.5 OCR Context (原始文本上下文)
<details>
<summary>点击展开查看提取的 UI 文本</summary>

### [Image 1/Page Name]
- **核心文案**：...
- **按钮 / CTA**：...
- **状态词**：...

</details>

## 0.6 视觉参考 (Visual Reference) [MANDATORY]
> [!NOTE]
> 引用 `raw/screenshots/ready/` 目录下的处理后截图，确保分析有据可依。

![页面描述](图片路径)
*图 1：[页面名称] - [核心交互说明]*

---

## 1. 页面矩阵与系统概览 (Page Matrix & Overview)

### 1.1 页面矩阵

| 页面 ID | 页面名称 | 页面角色 | 核心目标 | 入口线索 | 退出线索 | 视觉权重 |
|---|---|---|---|---|---|---|
| `page.home` | 战令主页 | hub | 展示轨道和主 CTA | 主入口按钮 | 购买弹层 / 返回 | P0 |

### 1.2 系统概览
- **单页系统**：描述该页面的核心功能、主要任务和唯一主路径。
- **多页系统**：描述页面之间的职责分工，例如“主页 / 任务页 / 奖励详情 / 购买页”。

---

## 2. 页面级信息架构 (Page-level IA)

### 2.1 页面 IA 树
为每个关键页面输出一棵 Mermaid `graph TD`，展示“页面 -> 区域 -> 组件”的层级。

### 2.2 空间区域拆解 (Spatial Region Breakdown)

> [!WARNING]
> 绝对禁止使用纯网页式的上下 DOM 分层思维（如 header/content/footer），必须将界面拆解为**游戏 HUD 空间结构**。

| 区域 ID | 所属页面 | 区域名称 | 空间槽位 (Spatial Slot) | 构图职责 | 主内容 | 阅读优先级 | 滚动方式 | 可观察证据 |
|---|---|---|---|---|---|---|---|---|
| `region.header` | `page.home` | 顶部状态区 | `top_bar` | 系统信息与资源 | 标题 / 货币 / 返回 | P0 | none | 图 1 |
| `region.main_stage` | `page.home` | 中央主舞台 | `center_stage` | 沉浸式美术重心 | 角色立绘 / 大尺寸奖品展示 | P0 | none | 图 1 |
| `region.action_panel` | `page.home` | 任务操作区 | `right_panel` | 密集信息与交互 | 任务条目 / 一键领取 | P0 | vertical | 图 1 |

**空间槽位 (Spatial Slot) 强制枚举字典**：
- `top_bar`：顶部统筹条（通常放置货币、返回键、标题）
- `left_rail`：左侧导航轨（通常放置全局系统切页 Tab）
- `center_stage`：中央主舞台（**极其重要：必须明确指出画面中哪里是无边框的大画幅视觉区域，严禁把全屏理解为卡片**）
- `center_panel`：中央内容面板（放置有边界的网格、列表）
- `right_panel`：右侧交互面板（放置任务、属性、高频操作 CTA）
- `bottom_bar`：底部操作条
- `overlay` / `modal`：覆盖层/弹层

**强制要求**：
- 必须明确拆分出至少一个带有“美术重心”职责的区域（如 `center_stage`），不要把游戏界面全描述成文字列表。
- 单页分析至少拆 3 个物理空间槽位。
- 多页分析至少拆出所有 P0 区域的空间映射。

---

## 3. 组件清单与状态线索 (Components & States)

### 3.1 组件清单

| component_id | 所属页面 | 所属区域 | 组件类型 | 文案/数据 | 状态线索 | 用户动作 | 证据 |
|---|---|---|---|---|---|---|---|
| `btn.claim_all` | `page.home` | `region.action_bar` | primary_button | 一键领取 | 可点 / 置灰 | tap | 图 1 |

### 3.2 状态表达
- 记录可见状态，如：`locked`、`claimable`、`claimed`、`selected`、`expired`。
- 记录状态切换证据，如：颜色变化、边框高亮、印章、置灰、角标、动效暗示。

---

## 4. 交互链路与导航推导 (Interaction & Navigation)

### 4.1 主路径
- 从玩家进入页面到完成核心任务，按顺序描述最短路径。

### 4.2 跳转关系表

| 来源页面 | 触发组件 | 目标页面/弹层 | 跳转类型 | 证据 |
|---|---|---|---|---|
| `page.home` | `btn.unlock` | `modal.purchase` | modal | 图 2 |

### 4.3 反馈闭环
- 核心操作完成后，系统如何反馈：
  - 视觉：扫光 / 飞入 / Toast / 弹层 / 印章
  - 文案：成功提示 / 状态更新
  - 数值：进度刷新 / 货币变化 / 可领奖励数量变化

---

## 5. 面向生成的线索提炼 (Generation-facing Notes)

**目标**：提炼可供 `skill 02` 消费的直接线索，而不是泛化的“好坏评价”。

### 5.1 页面生成线索

| 页面 ID | 主视觉焦点 | 信息阅读顺序 | 不可缺失组件 | 可后置组件 | 备注 |
|---|---|---|---|---|---|
| `page.home` | 奖励轨道 | 顶部状态 -> 轨道 -> 主 CTA | 进度、奖励格、主按钮 | 帮助入口 | 图 1 |

### 5.2 可疑点与待裁定
- 如果来源存在冲突，必须标注 `⚠️ 待裁定`，不得自行裁决。

### 5.3 次级 UX 诊断
- 可以记录亮点和潜在问题，但必须放在本节，且不得覆盖上文结构化内容。

---

## 6. 抽象定义 (Analysis Manifest)
```json
{
  "system_name": "String",
  "is_multi_page": true,
  "pages": [
    {
      "page_id": "page.home",
      "role": "hub",
      "regions": [
        {
          "region_id": "region.header",
          "position": "top",
          "components": ["title", "currency", "back_button"]
        }
      ]
    }
  ],
  "components": [
    {
      "component_id": "btn.claim_all",
      "type": "primary_button",
      "page_id": "page.home",
      "state_hints": ["enabled", "disabled"],
      "action_hints": ["claim_all"]
    }
  ],
  "navigation_hints": [
    {
      "from": "page.home",
      "trigger": "btn.unlock",
      "to": "modal.purchase"
    }
  ]
}
```

**强制要求**：
- `pages`、`components`、`navigation_hints` 不得为空。
- ID 命名必须与正文一致，方便下游直接引用。
