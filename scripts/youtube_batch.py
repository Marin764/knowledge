# -*- coding: utf-8 -*-
import sys
import os
import re
import json
import urllib.request
from pathlib import Path
from datetime import datetime
from urllib.parse import urlparse, parse_qs

# Force UTF-8 output on Windows
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

RAW_YOUTUBE_DIR = Path("raw/youtube")
LINKS_FILE = Path("youtu/链接.txt")

def extract_video_id(url):
    parsed = urlparse(url.strip())
    if parsed.hostname == 'youtu.be':
        return parsed.path[1:]
    if parsed.hostname in ('www.youtube.com', 'youtube.com'):
        if parsed.path == '/watch':
            return parse_qs(parsed.query)['v'][0]
        if '/shorts/' in parsed.path:
            return parsed.path.split('/')[-1]
    return None

def format_time(seconds):
    m, s = divmod(int(seconds), 60)
    return f"{m:02d}:{s:02d}"

def fetch_with_free_api(video_id):
    """Fallback using a free public API when IP is blocked"""
    try:
        # Use Piped API alternative which proxies requests
        url = f"https://api.piped.projectsegfau.lt/streams/{video_id}"
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            data = json.loads(response.read().decode())
            
        subtitles = data.get('subtitles', [])
        if not subtitles:
            return None
            
        # Try to find ZH or EN
        sub_url = None
        for sub in subtitles:
            if 'zh' in sub.get('code', '').lower():
                sub_url = sub.get('url')
                break
        
        if not sub_url:
            for sub in subtitles:
                if 'en' in sub.get('code', '').lower():
                    sub_url = sub.get('url')
                    break
                    
        if not sub_url and subtitles:
            sub_url = subtitles[0].get('url')
            
        if not sub_url:
            return None
            
        # Download the VTT content
        req = urllib.request.Request(sub_url, headers={'User-Agent': 'Mozilla/5.0'})
        with urllib.request.urlopen(req) as response:
            vtt_content = response.read().decode('utf-8')
            
        # Parse simple VTT manually
        lines = []
        block = []
        curr_time = 0
        
        for line in vtt_content.split('\n'):
            line = line.strip()
            if not line or '-->' in line or line.startswith('WEBVTT') or line.startswith('Kind:') or line.startswith('Language:'):
                if '-->' in line:
                    # Try to extract seconds
                    try:
                        ts = line.split('-->')[0].strip()
                        parts = ts.split(':')
                        s = float(parts[-1].replace(',', '.'))
                        m = int(parts[-2]) if len(parts) > 1 else 0
                        h = int(parts[-3]) if len(parts) > 2 else 0
                        new_time = h * 3600 + m * 60 + s
                        
                        if new_time - curr_time > 60 and block:
                            lines.append(f"[{format_time(curr_time)}] {' '.join(block)}")
                            block = []
                            curr_time = new_time
                    except:
                        pass
                continue
                
            text = re.sub(r'<[^>]+>', '', line).strip()
            if text:
                block.append(text)
                
        if block:
            lines.append(f"[{format_time(curr_time)}] {' '.join(block)}")
            
        return "\n\n".join(lines)
            
    except Exception as e:
        print(f"  Piped API failed: {e}")
        return None

def save_md(vid, title, content, url):
    RAW_YOUTUBE_DIR.mkdir(parents=True, exist_ok=True)
    safe_title = re.sub(r'[\/:*?"<>|]', "_", title)
    filepath = RAW_YOUTUBE_DIR / f"{safe_title}.md"
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

    updated_lines = []
    processed = 0

    print(f"[*] Processing {LINKS_FILE} ({len(lines)} lines)")

    for line in lines:
        line_stripped = line.strip()
        if not line_stripped or "已处理" in line_stripped or line_stripped.startswith("#"):
            updated_lines.append(line)
            continue

        parts = line_stripped.split(maxsplit=1)
        url = parts[0]
        title = parts[1].strip() if len(parts) > 1 else None

        vid = extract_video_id(url)
        if not vid:
            print(f"  SKIP: cannot parse video ID from: {url}")
            updated_lines.append(line)
            continue

        title = title or f"YouTube_{vid}"
        print(f"\n[*] {url}")
        print(f"    title: {title}")

        print("  Trying Piped API (IP block bypass)...")
        content = fetch_with_free_api(vid)
            
        if content:
            path = save_md(vid, title, content, url)
            print(f"    SAVED: {path}")
            updated_lines.append(f"{url} - {title} - [已处理]\n")
            processed += 1
        else:
            updated_lines.append(line)

    with open(LINKS_FILE, "w", encoding="utf-8") as f:
        f.writelines(updated_lines)

    print(f"\n[DONE] Processed: {processed}")

if __name__ == "__main__":
    main()
