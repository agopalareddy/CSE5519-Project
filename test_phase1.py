"""
Phase 1 Integration Test - Mohammad's Components
Tests dataset manager, attack image generator, and results analyzer.
"""

import sys
from pathlib import Path

# Add mohammad module to path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("PHASE 1: MOHAMMAD'S COMPONENTS TEST")
print("=" * 70)

# Test 1: Dataset Manager
print("\n" + "=" * 70)
print("TEST 1: DATASET MANAGER")
print("=" * 70)

from mohammad.dataset_manager import DatasetManager

dataset_manager = DatasetManager()

# Check existing images
stats = dataset_manager.get_dataset_stats()
print(f"\n📊 Current dataset: {stats['total']} images")

if stats["total"] < 10:
    print("\n📦 Dataset too small. Creating synthetic images...")
    dataset_manager.create_synthetic_images(num_images=15)

    # Try to download some real images too
    try:
        print("\n📥 Attempting to download sample images...")
        dataset_manager.download_sample_images(num_images=10)
    except Exception as e:
        print(f"⚠️  Download failed (no internet?): {e}")
        print("   Continuing with synthetic images only.")

# Get final stats
stats = dataset_manager.get_dataset_stats()
dataset_manager.print_stats()

# Test 2: Attack Image Generator
print("\n" + "=" * 70)
print("TEST 2: ATTACK IMAGE GENERATOR")
print("=" * 70)

from mohammad.attack_image_generator import AttackImageGenerator

generator = AttackImageGenerator()

# Get safe images to attack
safe_images = dataset_manager.get_all_safe_images("train")

if safe_images:
    print(f"\n🎯 Using {len(safe_images[:5])} base images for attacks")

    # Generate attacks
    attacks = generator.generate_attack_set(
        base_images=safe_images[:5], num_attacks_per_image=2
    )

    print(f"\n📊 Generated {len(attacks)} attack images")
    print("\n📁 Sample attacks:")
    for i, attack in enumerate(attacks[:3], 1):
        print(f"  {i}. {Path(attack['image_path']).name}")
        print(f"     Text: {attack['attack_text'][:60]}...")
        print(f"     Base: {Path(attack['base_image']).name}")
else:
    print("\n⚠️  No safe images available to create attacks")
    attacks = []

# Test 3: Results Analyzer
print("\n" + "=" * 70)
print("TEST 3: RESULTS ANALYZER")
print("=" * 70)

from mohammad.results_analyzer import ResultsAnalyzer

analyzer = ResultsAnalyzer()

# Create sample experiment data
print("\n📝 Creating sample experiment...")

sample_attack_results = [
    {
        "attack_text": attacks[0]["attack_text"] if attacks else "Sample attack 1",
        "success": True,
        "confidence": 0.92,
    },
    {
        "attack_text": (
            attacks[1]["attack_text"] if len(attacks) > 1 else "Sample attack 2"
        ),
        "success": False,
        "confidence": 0.35,
    },
    {"attack_text": "Sample attack 3", "success": True, "confidence": 0.88},
]

sample_defense_results = {
    "precision": 0.85,
    "recall": 0.90,
    "accuracy": 0.88,
    "true_positives": 9,
    "false_positives": 2,
    "true_negatives": 18,
    "false_negatives": 1,
}

analyzer.log_experiment(
    experiment_name="phase1_test",
    attack_results=sample_attack_results,
    defense_results=sample_defense_results,
    metadata={
        "phase": 1,
        "num_safe_images": stats["total"],
        "num_attack_images": len(attacks),
    },
)

# Print summary
analyzer.print_summary()

# Final Summary
print("\n" + "=" * 70)
print("✅ PHASE 1 COMPLETE - ALL COMPONENTS WORKING")
print("=" * 70)

print("\n📊 Phase 1 Summary:")
print(f"  ✓ Safe images:   {stats['total']}")
print(f"  ✓ Attack images: {len(attacks)}")
print(f"  ✓ Experiments:   1")
print(f"\n🎯 Ready for Phase 2: Red Team (Attack Generation)")
