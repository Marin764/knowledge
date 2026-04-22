import os
import argparse
from pathlib import Path
from PIL import Image
import imagehash

def preprocess_images(input_dir, output_dir, target_width=1280, hash_threshold=10, dedupe=False):
    """
    预处理游戏截图：去重（可选）、缩放、压缩。
    """
    input_path = Path(input_dir)
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    # 允许的图片格式
    extensions = {'.png', '.jpg', '.jpeg', '.webp'}
    image_files = [f for f in input_path.iterdir() if f.suffix.lower() in extensions]
    
    if not image_files:
        print(f"在 {input_dir} 中未找到图片文件。")
        return

    print(f"开始处理 {len(image_files)} 张图片...")
    if dedupe:
        print(f"已启用去重功能 (阈值: {hash_threshold})")
    else:
        print("去重功能已禁用，将处理所有图片。")

    processed_hashes = []
    skipped_count = 0
    saved_count = 0

    # 排序以保证处理的确定性
    image_files.sort()

    for img_file in image_files:
        try:
            with Image.open(img_file) as img:
                # 1. 检查去重 (仅在启用时执行)
                if dedupe:
                    curr_hash = imagehash.dhash(img)
                    is_duplicate = False
                    for prev_hash in processed_hashes:
                        if curr_hash - prev_hash <= hash_threshold:
                            is_duplicate = True
                            break
                    
                    if is_duplicate:
                        skipped_count += 1
                        continue
                    processed_hashes.append(curr_hash)

                # 2. 缩放处理
                w, h = img.size
                if w > target_width:
                    scale = target_width / float(w)
                    new_h = int(float(h) * scale)
                    img_resized = img.resize((target_width, new_h), Image.Resampling.LANCZOS)
                else:
                    img_resized = img

                # 3. 转换为 RGB
                if img_resized.mode in ("RGBA", "P"):
                    img_resized = img_resized.convert("RGB")

                # 4. 保存文件
                output_filename = img_file.stem + "_ready.jpg"
                save_path = output_path / output_filename
                img_resized.save(save_path, "JPEG", quality=85, optimize=True)
                
                saved_count += 1
                print(f"成功处理: {img_file.name} -> {output_filename}")

        except Exception as e:
            print(f"处理 {img_file.name} 时出错: {e}")

    print("\n" + "="*30)
    print(f"处理完成！")
    print(f"原始图片: {len(image_files)}")
    print(f"跳过重复: {skipped_count}")
    print(f"最终产出: {saved_count} 张图片位于 {output_dir}")
    print("="*30)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="游戏截图预处理脚本：去重与缩放")
    parser.add_argument("--input", default="raw/screenshots", help="输入截图目录")
    parser.add_argument("--output", default="raw/screenshots/ready", help="输出处理后图片目录")
    parser.add_argument("--width", type=int, default=1280, help="目标宽度 (默认 1280)")
    parser.add_argument("--threshold", type=int, default=10, help="去重哈希阈值 (默认 10)")
    parser.add_argument("--dedupe", action="store_true", help="启用感知哈希去重 (默认关闭)")
    
    args = parser.parse_args()
    
    preprocess_images(args.input, args.output, args.width, args.threshold, args.dedupe)
