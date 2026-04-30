# Skill 03：批量图片摄入、确权与图谱化流水线 (Batch Image Ingest, Verification & Atlas Solidification)

> **触发场景**：用户提供大量（≥20张）无序、异构或混杂的游戏截图。需要 AI 执行“语义筛选 → 确权 → 聚类 → 标准化 → 图谱化”的流水线。

---

## 0. 核心角色与原则 (Role & Principles)

你是一名**游戏 IA 研究员**兼 **UI 分类专家**。你的任务是通过 **AI 语义筛选**，从海量冗余截图中提炼出核心的**原型截图 (Archetypes)**，并在需要时继续把原型截图推进到**控件裁切与 atlas 图谱层**。

> [!TIP]
> **语义决策原则**：弃用低级的感知哈希（dhash）去重算法，由 AI 判定图片的交互价值。100 张原始图进，30 张具有决策意义的“原型真相”出；若目标包含后续界面生成，则继续从这些原型真相中抽取代表性控件，沉淀为 atlas 主参考层。

---

## 阶段 1：环境扫描与风险评估 (Scan & Audit)

### 1.1 目录预设
```
raw/screenshots/<游戏名>/          ← 原始 WebP/PNG（只读）
raw/screenshots/<游戏名>/mapping_log.md  ← 唯一真相映射表
assets/<game>_ui/                  ← 标准化资产库（JPEG, 语义化命名）
assets/<game>_controls/metadata/screens/  ← 截图级控件标注
assets/<game>_controls/crops/             ← 真实截图裁切控件
assets/<game>_controls/review/            ← BBox 与 contact sheet 复核图
assets/<game>_controls/metadata/atlas/    ← atlas 编排清单
assets/<game>_controls/atlas/             ← AI 可读控件图谱主产物
```

### 1.2 反模式告警 (Anti-Patterns)
- **严禁算法去重**：UI 背景高度统一时，算法会误删核心 Tab 页面。
- **防止账号污染**：必须通过右下角 UID 强制隔离不同账号的截图。

---

## 2. 视觉确权与“真相映射” (Visual Verification)

### 2.1 强制性视觉锚点检查
识别该批次的**视觉主键 (Visual PK)**：UID、语言版本、角色等级一致性。

### 2.2 建立唯一真相表 (Mapping Log)
在分发前记录每一张原型的映射关系。对于内容重复的截图，在日志中标注“重复项，不提取”。

```markdown
| 原始 ID | 视觉内容 (Content) | 视觉锚点 (UID) | 目标资产名 |
|:---|:---|:---|:---|
| 10106 | 角色主属性面板 | UID: 1032xxx | genshin-char-attributes.jpg |
| 10107 | 10106 的重复项 | UID: 1032xxx | [不提取] |
```

---

## 阶段 3：资产分发与物理转换 (Ingest & Convert)

### 3.1 AI 原型提取 (Archetype Extraction)
- AI 仅选择质量最高、状态最全的截图作为该 UI 状态的“原型”。
- 使用 Python 脚本执行物理找回：`Image.convert("RGB")` 仅转换选定的原型 ID。

### 3.2 标准命名规约
- 格式：`<游戏名>-<系统>-<子页面>.jpg`（全英文小写，语义化）。

---

## 阶段 4：控件拆解与 atlas 固化 (Controls & Atlas)

### 4.1 进入条件
- 当这批截图后续要用于 **AI 生成界面、风格重构、控件语法学习** 时，必须继续进入控件层。
- 如果本次目标仅是沉淀系统分析素材，可停留在 `assets/<game>_ui/`。

### 4.2 截图级控件标注
- 对已确权的原型截图建立 `manifest-*.json`。
- 每份标注至少记录：
  - `source`
  - `bbox`
  - `type`
  - `state`

### 4.3 真实裁切与复核
- 根据 `bbox` 批量导出真实裁切控件到 `crops/`。
- 同步生成 `annotated` 与 `contact-sheet` 到 `review/`，人工快速核对。
- `crops/` 是 atlas 的直接来源层，不再视作可删的中间文件。

### 4.4 atlas 图谱化
- 从 `crops/` 中筛选代表性控件，按类别组织到 `atlas/`。
- 使用 `metadata/atlas/manifest-*.json` 记录 atlas 中每个控件格子的分类、来源和说明。
- atlas 是给 AI 直接读取的主参考层，优先级高于单张原图。

---

## 处理流程 (The Workflow)

### 第一阶段：全量语义映射 (Full Semantic Mapping)
*   **动作**：AI 扫描整个 `raw/` 目录的所有原始 ID。
*   **要求**：在 `mapping_log.md` 中建立全量对照表。
*   **目标**：识别**“原型图（Archetypes）”**并标注**“冗余项”**。
*   **意义**：只有通过全量识别，才能在全局范围内判定哪些截图是重复的，哪些是具备分析价值的唯一原型，从而确保“确权”的完整性。

### 第二阶段：物理提取 (Archetype Extraction)
*   **动作**：根据映射表，运行 Python 脚本进行格式转换与同步。
*   **目标**：将杂乱 ID 转化为语义化文件名（如 `hsr-char-main.jpg`）存入 `assets/`。
*   **规格**：JPEG 格式，宽度限制在 1920px 以内，移除 Alpha 通道。

### 第三阶段：控件拆解 (Control Extraction)
*   **动作**：对确权后的原型图建立截图级控件标注，生成 `metadata/screens/`、`crops/` 与 `review/`。
*   **目标**：从整页截图中抽取代表性控件，为后续 AI 界面生成提供真实局部语法。
*   **说明**：如果本次目标只到分析，不强制进入此阶段；如果目标包含 AI 生成界面，则此阶段为必选。

### 第四阶段：图谱固化 (Atlas Solidification)
*   **动作**：基于 `crops/` 策展代表性控件，生成 `metadata/atlas/` 与 `atlas/`。
*   **目标**：形成 AI 可直接阅读的控件图谱大图，而不是继续追求单控件透明素材。
*   **主产物**：atlas 大图、atlas manifest。

### 第五阶段：知识固化 (Knowledge Solidification)
*   **动作**：引用 `assets/<game>_ui/` 中的语义化原型图，并在需要时参考 `atlas/`，编写 `wiki/analysis/` 下的系统分析报告。
*   **目标**：文图闭环，分析结论必须同时能回指系统级原型图，且在界面生成任务中可下钻到控件图谱层。

---

## 质量核查清单 (QA Checklist)

- [ ] **UID 隔离**：是否确认了所有资产均来自同一账号/版本？
- [ ] **语义匹配**：`assets/` 中的物理图片内容是否与文件名语义完全一致？
- [ ] **原型化原则**：是否已剔除重复截图，仅保留了最具代表性的原型？
- [ ] **控件层完整性**：若目标包含界面生成，是否已建立 `metadata/screens -> crops/review -> metadata/atlas -> atlas` 主链？
- [ ] **atlas-first 原则**：是否已明确 atlas 为 AI 主参考层，而不是继续扩散单控件透明导出？
- [ ] **引用安全**：Wiki 中是否全部使用相对于根目录的 Wikilink 格式？

---
<!-- v1.3: 废弃算法去重，确立 AI 语义筛选与原型提取 (Archetype Extraction) 机制 -->
<!-- v1.4: 将控件裁切、复核与 atlas 图谱层正式并入批量截图主链 -->
