# Skill 07: UI 图生图数据集构建 (Component Extraction & Labeling)

## 1. 目标 (Objective)
将游戏全屏截图转化为 AI（如 Stable Diffusion img2img、ControlNet、LoRA 训练）易于理解的结构化数据集。核心动作包括：**组件的物理裁切 (Cropping)**、**空间位置标注 (Spatial Layout)** 以及 **视觉与使用逻辑说明 (Semantic Usage)**。

## 2. 触发条件 (Trigger)
当用户明确要求“拆分 UI 控件”、“生成方便 AI 识别的图生图资料”、“标注布局与使用说明”时加载本技能。

## 3. 核心工作流 (Workflow)

### 阶段一：原子组件裁切定位 (Component Cropping)
- **原则**：剥离复杂的背景干扰，提取纯净的 UI 控件实体。
- **目标元素**：主操作按钮 (CTA)、底板面板 (Panels)、进度条/滑块、特殊边框 (Frames)、角色徽章/角标。
- **动作**：AI 不直接处理图片，而是通过分析截图，输出目标控件的 `[x, y, width, height]` BBox 坐标，供后续自动化脚本（如 `extract_ui_crops.ps1`）生成独立的纯净透明裁切图。

### 阶段二：空间布局与层级标注 (Layout Annotation)
- **原则**：记录组件在原始界面中的绝对位置与所在层级，为后续 AI 拼装或 ControlNet 提供空间约束。
- **属性**：
  - `layout_bbox`：绝对坐标，用于锁定位置。
  - `z_index` / `layer`：所处层级（如 `background`, `content_panel`, `modal_overlay`）。

### 阶段三：使用说明与提示词语义标注 (Usage & Prompt Labeling)
- **原则**：为每个被裁切的组件赋予详尽的“反向提示词 (Reverse Prompt)”，教导 AI 如何在图生图中重绘它。
- **必须包含的描述维度**：
  - `visual_style` (视觉特征)：材质（如木纹、金属、琉璃）、颜色基调、边框特征（如描金、发光）。
  - `interaction_state` (交互状态)：Normal（默认）, Hover（悬停）, Disabled（置灰）。
  - `usage_context` (业务用法)：该控件在系统中的职责（例如：“位于右下角，用于决定性的货币消耗操作”）。

## 4. 标准输出规范 (Output Schema)

执行此技能后，必须产出一份 JSON 格式的 `manifest-dataset.json`，结构如下：

```json
{
  "dataset_id": "game_name_ui_components",
  "base_resolution": [1920, 1080],
  "components": [
    {
      "id": "btn_primary_wood_gold",
      "crop_source": "assets/game_name_controls/crops/btn_primary.webp",
      "spatial": {
        "bbox": [1500, 900, 300, 80],
        "layer": "bottom_action_bar"
      },
      "semantics": {
        "visual_style": "深棕色胡桃木纹理底板，边缘有立体亮金色包边，中间带有微弱的高光扫过",
        "state": "normal",
        "usage_context": "用于高频的核心操作（如确认、出牌、购买），通常位于用户右手拇指舒适区"
      }
    }
  ]
}
```

## 5. 红线与限制 (Red Lines)
- **禁止过度开发展示层**：严格按照结构化数据 (JSON) 和说明文档 (Markdown) 输出，**绝对禁止**编写为了展示组件而创建的 HTML/CSS 网页界面。
- **描述必须具象化**：在 `visual_style` 中，严禁使用诸如“好看的按钮”、“古风背景”等模糊词汇，必须使用精确的 Prompt 级别词汇（如 `dark walnut texture`, `gold embossed border`, `drop shadow`）。
