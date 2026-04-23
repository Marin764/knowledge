# 知识库工具箱 (Scripts Library)

本目录包含用于自动化处理、Wiki 维护和资产管理的各种脚本。

## 目录结构

```text
scripts/
├── wiki.sh           # [主入口] 知识库维护 CLI 工具
├── images/           # 图片处理工具
│   ├── preprocess_images.py  # 截图预处理 (去重/缩放)
│   └── fix_genshin_assets.py # 原神 UI 资产确权修复脚本
├── fetchers/         # 外部资料抓取
│   ├── youtube_batch.py      # YouTube 字幕批量抓取 (主脚本)
│   └── yt_dlp_fetch.py       # 基于 yt-dlp 的视频信息获取
├── internal/         # 内部实现脚本 (供 wiki.sh 调用)
│   ├── lint.js               # 知识库健康检查
│   └── generate_slides.js    # Marp 幻灯片生成器
└── README.md         # 本文档
```

---

## 常用命令 (Wiki Helper)

建议通过根目录或 `scripts/` 运行 `bash scripts/wiki.sh`：

| 命令 | 用途 |
| :--- | :--- |
| `wiki lint` | 检查死链、孤立页面和 Frontmatter 错误 |
| `wiki stats` | 显示知识库当前规模统计 |
| `wiki slides --all` | 为所有 `concepts/` 页面生成幻灯片 |
| `wiki new concept <name>` | 使用标准模板创建新概念页面 |

---

## 专项工具说明

### 1. 图片处理 (images/)
- **preprocess_images.py**: 在摄入大量截图前运行，执行感知哈希去重。
- **fix_genshin_assets.py**: 针对原神项目的专项资产映射工具。

### 2. 字幕抓取 (fetchers/)
详细说明请参考 `scripts/fetchers/` 内部的相关文档。主要逻辑：
- 读取 `youtu/链接.txt`。
- 自动抓取并翻译字幕为中文。
- 生成 Markdown 存入 `raw/youtube/`。

---
*Last updated: 2026-04-23*
