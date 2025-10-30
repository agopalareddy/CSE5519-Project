"""
Dataset Manager - Safe Image Collection
Author: Mohammad Rouie Miab (implemented by Aadarsha)

Handles downloading and organizing safe/benign images for testing.
Uses multiple sources for diverse image sets.
"""

import os
import requests
import json
from pathlib import Path
from typing import List, Dict
from PIL import Image
import io


class DatasetManager:
    """Manages safe image datasets for defense testing."""

    def __init__(self, data_dir: str = "data/safe_images"):
        """
        Initialize the dataset manager.

        Args:
            data_dir: Directory to store safe images
        """
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.train_dir = self.data_dir / "train"
        self.val_dir = self.data_dir / "val"
        self.test_dir = self.data_dir / "test"

        for dir_path in [self.train_dir, self.val_dir, self.test_dir]:
            dir_path.mkdir(exist_ok=True)

    def download_sample_images(self, num_images: int = 20) -> List[str]:
        """
        Download sample images from Picsum (Lorem Ipsum for photos).
        This provides a diverse set of safe, royalty-free images.

        Args:
            num_images: Number of images to download

        Returns:
            List of paths to downloaded images
        """
        print(f"📥 Downloading {num_images} sample images...")
        downloaded_paths = []

        # Picsum provides random images with various dimensions
        image_sizes = [
            (400, 300),
            (500, 400),
            (600, 400),
            (800, 600),
            (640, 480),
            (1024, 768),
        ]

        for i in range(num_images):
            try:
                # Get a random size
                width, height = image_sizes[i % len(image_sizes)]
                url = f"https://picsum.photos/{width}/{height}?random={i}"

                response = requests.get(url, timeout=10)
                response.raise_for_status()

                # Save to appropriate split (70% train, 15% val, 15% test)
                if i < num_images * 0.7:
                    save_dir = self.train_dir
                    split = "train"
                elif i < num_images * 0.85:
                    save_dir = self.val_dir
                    split = "val"
                else:
                    save_dir = self.test_dir
                    split = "test"

                img_path = save_dir / f"safe_image_{i:03d}.jpg"

                # Save image
                img = Image.open(io.BytesIO(response.content))
                img.save(img_path, "JPEG")

                downloaded_paths.append(str(img_path))
                print(f"  ✓ Downloaded {split}/safe_image_{i:03d}.jpg")

            except Exception as e:
                print(f"  ✗ Failed to download image {i}: {e}")

        print(f"✅ Downloaded {len(downloaded_paths)} images successfully")
        return downloaded_paths

    def create_synthetic_images(self, num_images: int = 10) -> List[str]:
        """
        Create simple synthetic safe images (colored backgrounds, patterns).
        Useful for testing when internet is unavailable.

        Args:
            num_images: Number of synthetic images to create

        Returns:
            List of paths to created images
        """
        print(f"🎨 Creating {num_images} synthetic safe images...")
        created_paths = []

        colors = [
            (135, 206, 235),  # Sky blue
            (144, 238, 144),  # Light green
            (255, 182, 193),  # Light pink
            (221, 160, 221),  # Plum
            (255, 218, 185),  # Peach
            (176, 224, 230),  # Powder blue
        ]

        for i in range(num_images):
            try:
                # Create a simple colored image
                color = colors[i % len(colors)]
                img = Image.new("RGB", (640, 480), color)

                # Add some simple pattern (diagonal lines)
                from PIL import ImageDraw

                draw = ImageDraw.Draw(img)
                for j in range(0, 640, 40):
                    draw.line(
                        [(j, 0), (j + 480, 480)], fill=(255, 255, 255, 128), width=2
                    )

                # Save to train directory
                img_path = self.train_dir / f"synthetic_{i:03d}.jpg"
                img.save(img_path, "JPEG")

                created_paths.append(str(img_path))
                print(f"  ✓ Created synthetic_{i:03d}.jpg")

            except Exception as e:
                print(f"  ✗ Failed to create image {i}: {e}")

        print(f"✅ Created {len(created_paths)} synthetic images")
        return created_paths

    def get_all_safe_images(self, split: str = "all") -> List[str]:
        """
        Get paths to all safe images in a specific split.

        Args:
            split: One of 'train', 'val', 'test', or 'all'

        Returns:
            List of image paths
        """
        if split == "train":
            dirs = [self.train_dir]
        elif split == "val":
            dirs = [self.val_dir]
        elif split == "test":
            dirs = [self.test_dir]
        else:
            dirs = [self.train_dir, self.val_dir, self.test_dir]

        image_paths = []
        for dir_path in dirs:
            for ext in ["*.jpg", "*.jpeg", "*.png"]:
                image_paths.extend([str(p) for p in dir_path.glob(ext)])

        return sorted(image_paths)

    def get_dataset_stats(self) -> Dict:
        """
        Get statistics about the dataset.

        Returns:
            Dictionary with dataset statistics
        """
        train_images = self.get_all_safe_images("train")
        val_images = self.get_all_safe_images("val")
        test_images = self.get_all_safe_images("test")

        return {
            "total": len(train_images) + len(val_images) + len(test_images),
            "train": len(train_images),
            "val": len(val_images),
            "test": len(test_images),
            "train_paths": train_images[:5],  # First 5 as samples
            "val_paths": val_images[:5],
            "test_paths": test_images[:5],
        }

    def print_stats(self):
        """Print dataset statistics."""
        stats = self.get_dataset_stats()
        print("\n📊 Dataset Statistics:")
        print(f"  Total images: {stats['total']}")
        print(f"  Train split:  {stats['train']}")
        print(f"  Val split:    {stats['val']}")
        print(f"  Test split:   {stats['test']}")


if __name__ == "__main__":
    # Demo usage
    print("=" * 60)
    print("DATASET MANAGER DEMO")
    print("=" * 60)

    manager = DatasetManager()

    # Check if we already have images
    stats = manager.get_dataset_stats()
    if stats["total"] == 0:
        print("\n📦 No images found. Downloading sample dataset...")

        # Try to download from internet
        try:
            manager.download_sample_images(num_images=20)
        except Exception as e:
            print(f"⚠️  Internet download failed: {e}")
            print("📦 Creating synthetic images instead...")
            manager.create_synthetic_images(num_images=15)
    else:
        print(f"\n✓ Found existing dataset with {stats['total']} images")

    # Print final stats
    manager.print_stats()

    # Show sample paths
    print("\n📁 Sample image paths:")
    all_images = manager.get_all_safe_images()[:3]
    for path in all_images:
        print(f"  {path}")
