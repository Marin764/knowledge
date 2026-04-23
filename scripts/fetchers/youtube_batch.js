const fs = require('fs');
const path = require('path');
const https = require('https');

const LINKS_FILE = path.join(__dirname, '../youtu/链接.txt');
const RAW_DIR = path.join(__dirname, '../raw/youtube');

function extractVideoId(urlStr) {
    try {
        const parsed = new URL(urlStr);
        if (parsed.hostname === 'youtu.be') {
            return parsed.pathname.substring(1);
        } else if (parsed.hostname.includes('youtube.com')) {
            if (parsed.pathname === '/watch') {
                return parsed.searchParams.get('v');
            }
        }
    } catch (e) {
        return null;
    }
    return null;
}

// Write the python runner that forces the environment's python
async function main() {
    console.log(`📋 提示：你的环境中缺少 Python 的 youtube-transcript-api 库。`);
    console.log(`请先在终端运行：\npip install youtube-transcript-api\n\n然后在终端运行批量处理脚本：\npython scripts/youtube_batch.py`);
}

main();
