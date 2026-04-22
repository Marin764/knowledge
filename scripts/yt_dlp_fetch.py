# -*- coding: utf-8 -*-
"""
使用 yt-dlp 下载 YouTube 字幕，转换为 Markdown
"""
import sys
import os
import re
import subprocess
from pathlib import Path
from datetime import datetime

if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

import webvtt

LINKS_FILE = Path("youtu/链接.txt")
RAW_DIR = Path("raw/youtube")

def extract_video_id(url):
    """从 URL 提取视频 ID（去除时间参数）"""
    vid = re.search(r'[?&]v=([a-zA-Z0-9_-]{11})', url)
    if vid:
        return vid.group(1)
    vid = re.search(r'youtu\.be/([a-zA-Z0-9_-]{11})', url)
    if vid:
        return vid.group(1)
    return None

def format_time(seconds):
    m, s = divmod(int(float(seconds)), 60)
    return f"{m:02d}:{s:02d}"

def vtt_to_markdown(vtt_file, max_gap=60):
    """将 VTT 字幕文件转换为带时间戳的 Markdown，每分钟一个段落"""
    try:
        webvtt.from_file(vtt_file)
    except:
        return None

    lines = []
    block = []
    curr_time = 0
    first_ts = None

    for segment in webvtt.from_file(vtt_file):
        for line in segment.lines:
            text = line.strip()
            if not text:
                continue
            if first_ts is None:
                # 提取时间戳的秒数
                ts_parts = segment.start.split(':')
                if len(ts_parts) >= 3:
                    h, m, s = ts_parts[:3]
                    first_ts = int(h) * 3600 + int(m) * 60 + float(s.replace(',', '.'))

            # 近似时间，忽略小数
            ts_sec = 0
            try:
                ts_parts = segment.start.split(':')
                if len(ts_parts) == 3:
                    h, m, s = ts_parts
                    s = s.replace(',', '.')
                    ts_sec = int(h) * 3600 + int(m) * 60 + float(s)
            except:
                pass

            if ts_sec - curr_time > max_gap or not block:
                if block:
                    lines.append(f"[{format_time(curr_time)}] {' '.join(block)}")
                block = [text]
                curr_time = ts_sec
            else:
                block.append(text)

    if block:
        lines.append(f"[{format_time(curr_time)}] {' '.join(block)}")

    return "\n\n".join(lines)

def process_video(url):
    vid = extract_video_id(url)
    if not vid:
        print(f"  SKIP: cannot extract video ID")
        return None

    work_dir = Path("temp_ytdl")
    work_dir.mkdir(exist_ok=True)

    print(f"  Downloading subtitles via yt-dlp...")
    result = subprocess.run(
        [
            sys.executable, "-m", "yt_dlp",
            "--write-auto-sub", "--sub-lang", "zh-Hans,zh-Hant,zh,en",
            "--skip-download", "--convert-subs", "vtt",
            "-o", str(work_dir / vid),
            url
        ],
        capture_output=True, text=True
    )

    if result.returncode != 0:
        print(f"  ERROR: {result.stderr[:200] if result.stderr else 'unknown error'}")
        return None

    # 查找下载的 VTT 文件
    vtt_files = list(work_dir.glob(f"{vid}*.vtt"))
    if not vtt_files:
        print(f"  ERROR: no VTT file found")
        return None

    vtt_file = vtt_files[0]
    print(f"  Converting {vtt_file.name}...")

    md_content = vtt_to_markdown(str(vtt_file))
    if not md_content:
        print(f"  ERROR: failed to parse VTT")
        return None

    # 清理临时目录
    import shutil
    shutil.rmtree(work_dir, ignore_errors=True)

    return md_content

def save_md(vid, title, content, url):
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    safe_title = re.sub(r'[\/:*?"<>|]', "_", title)
    filepath = RAW_DIR / f"{safe_title}.md"
    date_str = datetime.now().strftime("%Y-%m-%d")
    fm = f"---\ntype: source\ntitle: \"{title}\"\nurl: \"{url}\"\ndate: {date_str}\nformat: [video]\nstatus: processed\n---\n\n# {title}\n\n"
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(fm + content)
    return filepath

def main():
    if not LINKS_FILE.exists():
        print(f"ERROR: not found: {LINKS_FILE}")
        return

    with open(LINKS_FILE, "r", encoding="utf-8") as f:
        lines = f.readlines()

    print(f"[*] Processing via yt-dlp ({len(lines)} links)")

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped or "已处理" in line_stripped or line_stripped.startswith("#"):
            continue

        parts = line_stripped.split(maxsplit=1)
        url = parts[0]
        title = parts[1].strip() if len(parts) > 1 else None

        vid = extract_video_id(url)
        if not vid:
            print(f"  SKIP: cannot parse: {url}")
            continue

        title = title or f"YouTube_{vid}"
        print(f"\n[*] {url}")
        print(f"    title: {title}")

        content = process_video(url)
        if content:
            path = save_md(vid, title, content, url)
            print(f"    SAVED: {path}")

            # 标记为已处理
            with open(LINKS_FILE, "r", encoding="utf-8") as f:
                content_l = f.read()
            content_l = content_l.replace(
                url,
                f"{url} - {title} - [已处理(yt-dlp)]"
            )
            with open(LINKS_FILE, "w", encoding="utf-8") as f:
                f.write(content_l)
        else:
            print(f"    FAILED, keeping original")

if __name__ == "__main__":
    main()
