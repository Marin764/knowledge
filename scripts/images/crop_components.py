import json
import os
from PIL import Image

def crop_components(dataset_json_path):
    """
    Reads the dataset JSON and crops the specified components from the source images.
    """
    if not os.path.exists(dataset_json_path):
        print(f"Error: Dataset JSON not found at {dataset_json_path}")
        return

    with open(dataset_json_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    # Base directory mappings (hardcoded for now based on project structure)
    # The JSON only has the target crop_source path, so we need to infer the original image.
    # For Phase 1, we map component IDs to their known source images.
    source_mapping = {
        "sgs_battle_avatar_left": "assets/three_kingdoms_kill_ui/sgs-battle-basic.webp",
        "sgs_battle_handcards_container": "assets/three_kingdoms_kill_ui/sgs-battle-basic.webp",
        "sgs_battle_action_btn": "assets/three_kingdoms_kill_ui/sgs-battle-basic.webp",
        "sgs_shop_item_card": "assets/three_kingdoms_kill_ui/sgs-shop-main.webp",
        "sgs_shop_category_tab": "assets/three_kingdoms_kill_ui/sgs-shop-main.webp",
        "sgs_shop_currency_bar": "assets/three_kingdoms_kill_ui/sgs-shop-main.webp",
        "sgs_hero_selection_card_active": "assets/three_kingdoms_kill_ui/sgs-hero-selection.webp",
        "sgs_hero_confirm_btn": "assets/three_kingdoms_kill_ui/sgs-hero-selection.webp",
        "sgs_hero_detail_panel": "assets/three_kingdoms_kill_ui/sgs-hero-selection.webp"
    }

    for component in data.get('components', []):
        comp_id = component.get('id')
        bbox = component.get('spatial', {}).get('bbox')
        crop_path = component.get('crop_source')
        
        if comp_id not in source_mapping:
            print(f"Warning: No source image mapped for {comp_id}. Skipping.")
            continue

        source_img_path = source_mapping[comp_id]

        if not bbox or len(bbox) != 4:
            print(f"Warning: Invalid bbox for {comp_id}. Skipping.")
            continue
            
        if not os.path.exists(source_img_path):
            print(f"Warning: Source image {source_img_path} not found. Skipping {comp_id}.")
            continue

        x, y, w, h = bbox
        
        try:
            # Ensure crop directory exists
            os.makedirs(os.path.dirname(crop_path), exist_ok=True)
            
            with Image.open(source_img_path) as img:
                # PIL crop expects (left, upper, right, lower)
                cropped_img = img.crop((x, y, x + w, y + h))
                cropped_img.save(crop_path)
                print(f"Success: Cropped and saved {comp_id} to {crop_path}")
        except Exception as e:
            print(f"Error processing {comp_id}: {e}")

if __name__ == "__main__":
    # Ensure this is run from the project root (know folder)
    json_path = "assets/three_kingdoms_kill_controls/metadata/components/sgs-img2img-dataset-v1.json"
    crop_components(json_path)
