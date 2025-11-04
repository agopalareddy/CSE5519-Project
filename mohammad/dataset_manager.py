"""
Dataset Manager - Safe Image Collection
Author: Mohammad Rouie Miab (implemented by Aadarsha; updated by Mohammad Rouie Miab)

One big dataset.
- Preselects a random set of image IDs from COCO 2017
- Downloads exactly those images from the official COCO image server
- Exposes a PyTorch Dataset to use the pool in training/eval code
"""

import os
import requests
import json
from pathlib import Path
from typing import List, Dict
from PIL import Image
import io
import random
from concurrent.futures import ThreadPoolExecutor, as_completed

from torch.utils.data import Dataset
from torchvision import transforms as T
from pycocotools.coco import COCO

COCO_DATASET_BASE_URL = "http://images.cocodataset.org" # format: BASE + "{split}2017/{image_id:012d}.jpg"
COCO_ANNOTATIONS_URL = "https://images.cocodataset.org/annotations/annotations_trainval2017.zip"
DEFAULT_DATASET_SPLIT = "train"
DEFAULT_DATASET_DIR = "../data/coco2017_safe_images"


class COCODataset(Dataset):
    """PyTorch Dataset for the COCO 2017 safe image pool."""

    def __init__(self, root_dir: str, transform: T.Compose | None = None):
        """
        Initialize the COCO dataset.

        Parameters
        ----------
        root_dir : str
            Directory with all the images.
        transform : T.Compose | None, optional
            Optional transform to be applied on a sample, default: None

        Raises
        ------
        RuntimeError
            If no images are found in the root directory.
            (Run DatasetManager.download_coco_images() first.)
        """
        self.root_dir: Path = Path(root_dir)
        self.img_paths: list[Path] = sorted([p for p in self.root_dir.glob("*.jpg")])
        self.transform: T.Compose | None = transform

        if len(self.img_paths) == 0:
            raise RuntimeError(
                f"No images found in {self.root_dir}.\nRun DatasetManager.download_coco_images()."
            )

    def __len__(self):
        """Return the number of images in the dataset."""
        return len(self.img_paths)

    def __getitem__(self, idx: int):
        """Return the image and its path."""
        img_path = self.img_paths[idx]
        img = Image.open(img_path).convert("RGB")
        if self.transform:
            img = self.transform(img)
        # just return the image and its path (or None as target)
        return img, str(img_path)

class DatasetManager:
    """Manages safe image datasets for defense testing."""

    """
    Typical usage:
    1. Initialize the manager:
        manager = DatasetManager(data_dir="path/to/data", split="train")
    2. Preselect image IDs:
        selected_ids = manager.preselect_image_ids(num_images=100, seed=1)
    3. Download the images:
        manager.download_coco_images(selected_ids)
    4. Access dataset statistics:
        manager.print_dataset_stats()
    5. View sample images:
        manager.view_sample_images(num_samples=5)
    6. Build a PyTorch Dataset:
        dataset = manager.build_torch_dataset(transform=your_transform)
    """

    def __init__(self, data_dir: str = DEFAULT_DATASET_DIR, split: str = DEFAULT_DATASET_SPLIT):
        """
        Initialize the DatasetManager.

        Parameters
        ----------
        data_dir : str, optional
            Directory to store the dataset, default: `DEFAULT_DATASET_DIR`
        split : str, optional
            Dataset split: "train" or "val", default: `DEFAULT_DATASET_SPLIT`
        """
        self.base_dir: Path = Path(data_dir)
        self.images_dir: Path = self.base_dir / "images"
        self.meta_dir: Path = self.base_dir / "meta"
        self.annotations_dir: Path = self.base_dir / "annotations"
        self.preselection_path: Path = self.meta_dir / f"preselected_images_{split}.json"  # Preselected image IDs

        self.split: str = split  # "train" or "val"

        # Create dirs
        self.images_dir.mkdir(parents=True, exist_ok=True)
        self.meta_dir.mkdir(parents=True, exist_ok=True)
        self.annotations_dir.mkdir(parents=True, exist_ok=True)

    def preselect_image_ids(
        self,
        num_images: int = 100,
        seed: int = 1,
        save_to_file: bool = True,
        annotations_path: str | None = None,
    ) -> List[int]:
        """
        Preselect (deterministically) random image IDs from COCO dataset.

        Parameters
        ----------
        num_images : int, optional
            Number of images to preselect, default: 100
        seed : int, optional
            Random seed for reproducibility, default: 1
        save_to_file : bool, optional
            Whether to save the preselected image IDs to a file, default: True
        annotations_path : str | None, optional
            Path to the COCO annotations JSON file, by default None
            (If None, uses the default annotations path of `self.data_dir`/annotations/instances_{split}2017.json)

        Returns
        -------
        List[int]
            List of preselected image IDs.

        Raises
        ------
        FileNotFoundError
            If the annotations file is not found.
            If this is the case, download COCO annotations from the official source:
            https://images.cocodataset.org/annotations/annotations_trainval2017.zip
            and place the appropriate split's json it in the '`self.data_dir`/annotations' directory.
        Warning
            If the requested number of images exceeds the available images.
        """
        annotations_file: Path = (
            Path(annotations_path)
            if annotations_path
            else self.base_dir / "annotations" / f"instances_{self.split}2017.json"
        )
        if not annotations_file.exists():
            raise FileNotFoundError(
                f"Annotations file not found: {annotations_file}\n"
                "Please provide a valid path or download COCO annotations from the official source: "
                f"{COCO_ANNOTATIONS_URL}"
                f" and place the appropriate split's json it in the '{self.base_dir / 'annotations'}' directory."
            )

        rng = random.Random(seed)

        coco = COCO(annotations_file)
        all_img_ids: List[int] = coco.getImgIds()

        if num_images > len(all_img_ids):
            raise Warning(
                f"Requested {num_images} images, but only {len(all_img_ids)} available.\n"
                "Selecting all available images."
            )

        num_images = min(num_images, len(all_img_ids))
        selected_img_ids: List[int] = rng.sample(all_img_ids, k=num_images)

        if save_to_file:
            with open(self.preselection_path, "w") as f:
                json.dump(
                    {
                        "split": self.split,
                        "num_images": num_images,
                        "seed": seed,
                        "image_ids": selected_img_ids,
                    },
                    f,
                    indent=4,
                )
            print(f"Preselected {num_images} image IDs and info saved to {self.preselection_path}.")

        return selected_img_ids

    def load_preselected_image_ids(self) -> List[int]:
        """
        Load preselected image IDs from file.

        Returns
        -------
        List[int]
            List of preselected image IDs.

        Raises
        ------
        FileNotFoundError
            If the preselection file is not found.
            If this is the case, run preselect_image_ids() first.
        """
        if not self.preselection_path.exists():
            raise FileNotFoundError(
                f"Preselection file not found: {self.preselection_path}\n"
                "Run preselect_image_ids()."
            )

        with open(self.preselection_path, "r") as f:
            data: dict = json.load(f)

        return [int(i) for i in data["image_ids"]]

    def download_coco_images(
        self,
        image_ids: List[int],
        max_workers: int = 8,
        timeout: int = 20,
    ) -> List[str]:
        """
        Download preselected COCO images.

        Parameters
        ----------
        image_ids : List[int]
            List of image IDs to download.
        max_workers : int, optional
            Number of concurrent download threads, default: 8
        timeout : int, optional
            Timeout (seconds) for each download request, by default 20

        Returns
        -------
        List[str]
            List of paths to downloaded images
        """
        self.images_dir.mkdir(parents=True, exist_ok=True)

        # Single-image downloader for threading
        def download_one_image(img_id: int) -> str | None:
            img_url: str = f"{COCO_DATASET_BASE_URL}/{self.split}2017/{img_id:012d}.jpg"
            output_img_path: Path = self.images_dir / f"{img_id:012d}.jpg"

            if output_img_path.exists() and output_img_path.stat().st_size > 0:  # Already downloaded w/ data
                print(f"Image {img_id:012d} already exists, skipping download...")
                return str(output_img_path)

            try:
                response = requests.get(img_url, timeout=timeout)
                response.raise_for_status()

                image = Image.open(io.BytesIO(response.content)).convert("RGB")
                image.save(output_img_path, "JPEG")
                print(f"Successfully downloaded: {output_img_path}")
                return str(output_img_path)
            except Exception as e:
                print(f"Failed to download image {img_id:012d}: {e}")
                return str(output_img_path)

        # Download images in parallel
        downloaded_paths: List[str] = []
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures: dict = {executor.submit(download_one_image, image_id): image_id for image_id in image_ids}
            for future in as_completed(futures):
                result_path = future.result()
                if result_path:
                    downloaded_paths.append(result_path)

        print(f"--- Download complete ---\n{len(downloaded_paths)}/{len(image_ids)} images downloaded.")
        print(f"Images saved to: {self.images_dir}")
        return downloaded_paths

    def get_image_paths(self) -> List[str]:
        """
        Get paths to all downloaded images.

        Returns
        -------
        List[str]
            List of image paths
        """
        image_paths = [
            str(p) for p in self.images_dir.glob("*.jpg")
        ]
        return sorted(image_paths)

    def get_dataset_stats(self) -> Dict:
        """
        Get statistics about the dataset.

        Returns
        -------
        Dict
            Dictionary with dataset statistics
        """
        image_paths: List[str] = self.get_image_paths()
        stats: Dict = {
            "total_images": len(image_paths),
            "sample_path": image_paths[0],  # First image path as sample
            "data_dir": str(self.images_dir),
            "split": self.split,
        }
        return stats

    def print_dataset_stats(self):
        """Print dataset statistics."""
        stats = self.get_dataset_stats()
        print(f"Dataset Statistics and Info:")
        print(f"  Split: {stats['split']}")
        print(f"  Total Images: {stats['total_images']}")
        print(f"  Data Directory: {stats['data_dir']}")
        print(f"  Sample Image Path: {stats['sample_path']}")

    def view_sample_images(self, num_samples: int = 3):
        """
        View sample images from the dataset.

        Parameters
        ----------
        num_samples : int, optional
            Number of sample images to display, default: 3
        """
        image_paths: List[str] = self.get_image_paths()
        sample_paths: List[str] = random.sample(image_paths, min(num_samples, len(image_paths)))

        for img_path in sample_paths:
            img = Image.open(img_path).convert("RGB")
            img.show(title=f"Sample Image: {img_path}")

    def build_torch_dataset(self, transform: T.Compose | None = None) -> Dataset:
        """
        Build a PyTorch Dataset for the downloaded images.

        Parameters
        ----------
        transform : T.Compose | None, optional
            Transformations to apply to the images, default: None

        Returns
        -------
        Dataset
            PyTorch Dataset of downloaded images
        """
        return COCODataset(root_dir=str(self.images_dir), transform=transform)


if __name__ == "__main__":
    # Demo usage
    manager = DatasetManager()
    selected_ids: List[int] = manager.preselect_image_ids()
    manager.download_coco_images(selected_ids)
    manager.print_dataset_stats()
    manager.view_sample_images()
    dataset: Dataset = manager.build_torch_dataset()

    # Verify dataset and view a sample with torch
    print(f"Built PyTorch Dataset with {len(dataset)} images.")
    sample_img, sample_path = dataset[0]
    print(f"Sample image shape: {sample_img.size}, path: {sample_path}")
    sample_img.show(title="Sample Image from PyTorch Dataset")
