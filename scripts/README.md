# YouTube 字幕批量处理工具

抓取 YouTube 视频字幕，转换为 Markdown 格式，存入本地知识库。

## 环境要求

- Python 3.12+
- `youtube-transcript-api`

```bash
# 安装依赖
pip install youtube-transcript-api
```

## 目录结构

```
know/
├── youtu/
│   └── 链接.txt          # 链接列表（每行一个链接）
├── raw/
│   └── youtube/          # 字幕输出目录
└── scripts/
    ├── youtube_batch.py  # 批量处理脚本（主脚本）
    └── README.md         # 本文档
```

## 链接文件格式

`youtu/链接.txt` 每行一个链接，支持格式：

```txt
https://www.youtube.com/watch?v=iIOIT3dCy5w
https://www.youtube.com/watch?v=7L8vAGGitr8 视频标题（可选）
https://youtu.be/P05ONfLOqmY
```

- 第一列：YouTube 链接（支持标准链接、youtu.be 短链接）
- 第二列（可选）：视频标题（留空则自动用 Video ID）
- 时间参数（`&t=xxx`）会被自动忽略

## 使用方法

```bash
# 方式1: 直接运行
python scripts/youtube_batch.py

# 方式2: 使用完整路径
"C:\Users\xxx\AppData\Local\Programs\Python\Python312\python.exe" scripts/youtube_batch.py
```

## 工作流程

```
链接文件 → 解析 Video ID → 请求字幕 → 格式转换 → 输出 Markdown
```

1. **URL 解析**：从链接中提取 11 位 Video ID
2. **字幕获取**：优先中文字幕 → 英/日文翻译为中文 → 任意可用语言
3. **格式转换**：VTT 原始数据 → 每分钟一个段落的 Markdown
4. **写入文件**：保存到 `raw/youtube/视频标题.md`
5. **标记状态**：在 `链接.txt` 对应行末尾追加 ` - [已处理]`

## 输出格式

生成的 Markdown 文件包含标准 Frontmatter：

```yaml
---
type: source
title: "视频标题"
url: "https://www.youtube.com/watch?v=xxx"
date: 2026-04-17
format: [video]
status: processed
---

# 视频标题

[00:00] 欢迎大家来到今天的节目
今天我们要讲的是游戏交互设计

[01:05] 第一个核心原则是响应感
玩家按下按键到画面反馈的时间窗口
```

## 注意事项

- **IP 限制**：频繁请求可能导致 YouTube 临时封禁 IP，等待几十分钟后重试
- **已处理跳过**：脚本会自动跳过标记为 `[已处理]` 的链接
- **中文优先**：优先获取中文/翻译字幕，纯英文内容质量取决于 YouTube 自动翻译
- **UTF-8 编码**：Windows 环境下强制 UTF-8 输出，避免中文乱码

## 故障排除

### YouTube IP 封禁

```
ERROR: YouTube is blocking requests from your IP
```

等待 30-60 分钟后重试，或尝试使用 VPN 更换出口 IP。

### 无字幕可用

部分视频（多为用户生成内容）可能没有字幕，脚本会保留该链接不处理。

### JavaScript 运行时警告（yt-dlp 模式）

```
No supported JavaScript runtime could be found
```

安装 Node.js 即可解决，不影响默认 API 模式。

## 许可证

MIT License
