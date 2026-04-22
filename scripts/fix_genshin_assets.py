import os
from pathlib import Path
from PIL import Image

# 定义映射关系 (Original ID -> Target Name)
mapping = {
    "10106": "genshin-char-attributes.jpg",
    "10112": "genshin-growth-weapon.jpg",
    "10114": "genshin-growth-artifact.jpg",
    "10116": "genshin-growth-constellation.jpg",
    "10118": "genshin-growth-talent.jpg",
    "10119": "genshin-growth-talent-detail.jpg",
    "10109": "genshin-growth-material-preview.jpg",
    "10110": "genshin-char-outfit.jpg",
    "10111": "genshin-char-glider.jpg",
    "10139": "genshin-main-menu.jpg",
    "10142": "genshin-profile-details.jpg",
    "10138": "genshin-map-view.jpg",
    "10090": "genshin-inventory-artifacts.jpg",
    "10091": "genshin-inventory-materials.jpg",
    "10100": "genshin-weapon-refine.jpg",
    "10102": "genshin-weapon-details.jpg",
    "10092": "genshin-inventory-food.jpg",
    "10089": "genshin-inventory-weapons.jpg",
    "10096": "genshin-inventory-batch-destroy.jpg",
    "10081": "genshin-wish-char-banner.jpg",
    "10082": "genshin-wish-weapon-banner.jpg",
    "10083": "genshin-wish-standard-banner.jpg",
    "10084": "genshin-wish-result-single.jpg",
    "10138": "genshin-map-teleport.jpg",
    "10135": "genshin-map-markers.jpg",
    "10136": "genshin-map-general.jpg"
}

# 路径定义
raw_dir = Path(r"c:\Users\hutingrong\Desktop\know\raw\genshin\www.gameui.net\原神-GameUI.net")
target_dir = Path(r"c:\Users\hutingrong\Desktop\know\assets\genshin_ui")

target_dir.mkdir(parents=True, exist_ok=True)

print("开始物理找回资产...")

for orig_id, target_name in mapping.items():
    source_file = raw_dir / f"{orig_id}.webp"
    dest_file = target_dir / target_name
    
    if source_file.exists():
        try:
            with Image.open(source_file) as img:
                img = img.convert("RGB")
                img.save(dest_file, "JPEG", quality=90)
            print(f"成功: {orig_id}.webp -> {target_name}")
        except Exception as e:
            print(f"转换失败 {orig_id}: {e}")
    else:
        print(f"未找到原始文件: {source_file}")

print("资产找回完成。")
