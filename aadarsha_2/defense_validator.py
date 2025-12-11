"""Validates defense scripts against test image sets (malicious and benign)."""

import importlib.util
import sys
from pathlib import Path
from typing import List, Dict, Any


class DefenseValidator:
    """Validates defense scripts against test images."""

    def __init__(self):
        self.results = []

    def load_defense_script(self, script_path: str):
        """
        Dynamically load a Python defense script.

        Args:
            script_path: Path to the defense script

        Returns:
            Loaded module containing detect_attack function
        """
        spec = importlib.util.spec_from_file_location("defense_module", script_path)
        module = importlib.util.module_from_spec(spec)
        sys.modules["defense_module"] = module
        spec.loader.exec_module(module)

        if not hasattr(module, "detect_attack"):
            raise ValueError("Defense script must have a 'detect_attack' function")

        return module

    def validate_defense(
        self,
        defense_script_path: str,
        malicious_images: List[str],
        benign_images: List[str],
    ) -> Dict[str, Any]:
        """
        Test a defense script against malicious and benign images.

        Args:
            defense_script_path: Path to the Python defense script
            malicious_images: List of paths to attack images (should be detected)
            benign_images: List of paths to safe images (should NOT be detected)

        Returns:
            Dictionary with precision, recall, accuracy, and detailed results
        """
        try:
            defense_module = self.load_defense_script(defense_script_path)
        except Exception as e:
            return {
                "error": f"Failed to load defense script: {str(e)}",
                "precision": 0.0,
                "recall": 0.0,
                "accuracy": 0.0,
            }

        true_positives = 0  # Correctly detected attacks
        false_positives = 0  # Benign flagged as attack
        true_negatives = 0  # Correctly allowed benign
        false_negatives = 0  # Missed attacks

        # Store detailed results for verbose output
        detailed_results = []

        # Test against malicious images
        print("\n  Testing malicious images:")
        for img_path in malicious_images:
            try:
                is_attack = defense_module.detect_attack(img_path)
                # Try to get OCR text for verbose output
                ocr_text = ""
                if hasattr(defense_module, "extract_text_from_image"):
                    try:
                        ocr_text = defense_module.extract_text_from_image(img_path)
                        ocr_text = (
                            ocr_text[:100] + "..." if len(ocr_text) > 100 else ocr_text
                        )
                    except:
                        ocr_text = "(OCR failed)"

                status = "✓ DETECTED" if is_attack else "✗ MISSED"
                print(f"    {status}: {Path(img_path).name}")
                if ocr_text:
                    print(f"      OCR: {ocr_text}")

                if is_attack:
                    true_positives += 1
                else:
                    false_negatives += 1

                detailed_results.append(
                    {
                        "path": img_path,
                        "type": "malicious",
                        "detected": is_attack,
                        "ocr_text": ocr_text,
                    }
                )
            except Exception as e:
                print(f"    ✗ ERROR: {Path(img_path).name} - {e}")
                false_negatives += 1

        # Test against benign images
        print("\n  Testing benign images:")
        for img_path in benign_images:
            try:
                is_attack = defense_module.detect_attack(img_path)
                # Try to get OCR text for verbose output
                ocr_text = ""
                if hasattr(defense_module, "extract_text_from_image"):
                    try:
                        ocr_text = defense_module.extract_text_from_image(img_path)
                        ocr_text = (
                            ocr_text[:100] + "..." if len(ocr_text) > 100 else ocr_text
                        )
                    except:
                        ocr_text = "(OCR failed)"

                status = "✓ SAFE" if not is_attack else "✗ FALSE POSITIVE"
                print(f"    {status}: {Path(img_path).name}")
                if ocr_text and ocr_text.strip():
                    print(f"      OCR: {ocr_text}")

                if is_attack:
                    false_positives += 1
                else:
                    true_negatives += 1

                detailed_results.append(
                    {
                        "path": img_path,
                        "type": "benign",
                        "detected": is_attack,
                        "ocr_text": ocr_text,
                    }
                )
            except Exception as e:
                print(f"    ✗ ERROR: {Path(img_path).name} - {e}")
                false_positives += 1

        # Calculate metrics
        total = len(malicious_images) + len(benign_images)
        precision = (
            true_positives / (true_positives + false_positives)
            if (true_positives + false_positives) > 0
            else 0
        )
        recall = (
            true_positives / (true_positives + false_negatives)
            if (true_positives + false_negatives) > 0
            else 0
        )
        accuracy = (true_positives + true_negatives) / total if total > 0 else 0

        return {
            "precision": precision,
            "recall": recall,
            "accuracy": accuracy,
            "true_positives": true_positives,
            "false_positives": false_positives,
            "true_negatives": true_negatives,
            "false_negatives": false_negatives,
            "total_malicious": len(malicious_images),
            "total_benign": len(benign_images),
        }

    def print_results(self, results: Dict[str, Any]):
        """Pretty print validation results."""
        print("\n=== Defense Validation Results ===")
        if "error" in results:
            print(f"ERROR: {results['error']}")
            return

        print(f"Accuracy:  {results['accuracy']:.2%}")
        print(f"Precision: {results['precision']:.2%}")
        print(f"Recall:    {results['recall']:.2%}")
        print(f"\nConfusion Matrix:")
        print(
            f"  True Positives:  {results['true_positives']} / {results['total_malicious']}"
        )
        print(
            f"  False Negatives: {results['false_negatives']} / {results['total_malicious']}"
        )
        print(
            f"  True Negatives:  {results['true_negatives']} / {results['total_benign']}"
        )
        print(
            f"  False Positives: {results['false_positives']} / {results['total_benign']}"
        )
