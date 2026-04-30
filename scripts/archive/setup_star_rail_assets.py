from pathlib import Path
from PIL import Image

mapping = {
    "10115": "hsr-hub-phone-menu.jpg",
    "10015": "hsr-map-xianzhou-overview.jpg",
    "10200": "hsr-map-navigation.jpg",
    "10185": "hsr-map-healing-anchor.jpg",
    "1918517": "hsr-wish-stellar-warp.jpg",
    "10217": "hsr-wish-lightcone-warp.jpg",
    "10186": "hsr-wish-result-single.jpg",
    "10075": "hsr-char-attributes.jpg",
    "10116": "hsr-growth-ascension.jpg",
    "10108": "hsr-growth-lc-ascension.jpg",
    "10210": "hsr-growth-lightcone.jpg",
    "10113": "hsr-growth-relic-detail.jpg",
    "10109": "hsr-growth-relic-slots.jpg",
    "10229": "hsr-combat-hud-boss.jpg",
    "10145": "hsr-combat-tutorial-kafka.jpg",
    "10105": "hsr-system-synthesis.jpg",
    "10065": "hsr-system-friend-support.jpg",
    "10120": "hsr-system-mission-log.jpg",
    "10118": "hsr-interaction-item-submit.jpg",
    "10070": "hsr-sim-universe-path-select.jpg",
    "10126": "hsr-sim-universe-path-map.jpg",
    "10050": "hsr-sim-universe-hub.jpg",
    "10245": "hsr-sim-universe-blessing.jpg",
    "10320": "hsr-shop-main.jpg",
    "10300": "hsr-shop-world.jpg",
    "10220": "hsr-event-list.jpg"
}

raw_dir = Path(r"c:\Users\hutingrong\Desktop\know\raw\崩坏：星穹铁道-GameUI.net")
target_dir = Path(r"c:\Users\hutingrong\Desktop\know\assets\star_rail_ui")
target_dir.mkdir(parents=True, exist_ok=True)

print("Starting Star Rail Archetype Extraction V1.2 (Full Scan)...")

for original_id, target_name in mapping.items():
    source_path = raw_dir / f"{original_id}.webp"
    if not source_path.exists():
        source_path = raw_dir / f"{original_id}.png"
    
    if source_path.exists():
        print(f"  - Processing: {original_id} -> {target_name}")
        with Image.open(source_path) as img:
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")
            if img.width > 1920:
                ratio = 1920 / img.width
                new_size = (1920, int(img.height * ratio))
                img = img.resize(new_size, Image.LANCZOS)
            img.save(target_dir / target_name, "JPEG", quality=85)
    else:
        print(f"  - Warning: Source file {original_id} not found")

print("V1.2 Sync Complete! Total Archetypes: 26")
