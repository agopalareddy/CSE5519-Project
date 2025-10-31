"""
Visual Demo - Show Sample Images
Displays information about safe and attack images.
"""

from pathlib import Path
from PIL import Image

print("=" * 70)
print("PHASE 1 - VISUAL DEMO")
print("=" * 70)

# Show safe images info
safe_dir = Path("data/safe_images/train")
safe_images = list(safe_dir.glob("*.jpg"))[:5]

print("\n📷 SAFE IMAGES SAMPLE:")
print("-" * 70)
for img_path in safe_images:
    with Image.open(img_path) as img:
        print(f"✓ {img_path.name}")
        print(f"  Size: {img.size[0]}x{img.size[1]} pixels")
        print(f"  Mode: {img.mode}")
        print(f"  File size: {img_path.stat().st_size // 1024}KB")
        print()

# Show attack images info
attack_dir = Path("data/attack_images")
attack_images = list(attack_dir.glob("*.jpg"))[:5]

print("\n🔴 ATTACK IMAGES SAMPLE:")
print("-" * 70)
for img_path in attack_images:
    with Image.open(img_path) as img:
        print(f"✓ {img_path.name}")
        print(f"  Size: {img.size[0]}x{img.size[1]} pixels")
        print(f"  Mode: {img.mode}")
        print(f"  File size: {img_path.stat().st_size // 1024}KB")

        # Extract attack info from filename
        base_name = img_path.stem.replace("attack_", "").rsplit("_", 1)[0]
        print(f"  Based on: {base_name}.jpg")
        print(f"  ⚠️  Contains embedded attack prompt")
        print()

print("=" * 70)
print("✅ All images generated successfully!")
print("=" * 70)
print("\n💡 Tip: Open the images in data/attack_images/ to see the")
print("   embedded attack text overlays!")
