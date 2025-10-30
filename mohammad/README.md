# Mohammad's Components

This directory contains the data management and analysis components.

## Files

### `dataset_manager.py`
Manages safe/benign image datasets:
- Downloads sample images from Picsum (Lorem Ipsum for photos)
- Creates synthetic safe images
- Organizes into train/val/test splits
- Provides dataset statistics

**Usage:**
```python
from mohammad.dataset_manager import DatasetManager

manager = DatasetManager()
manager.download_sample_images(num_images=20)
safe_images = manager.get_all_safe_images()
```

**CLI:**
```bash
python mohammad/dataset_manager.py
```

### `attack_image_generator.py`
Creates attack images with embedded prompts:
- Text overlay attacks (visible prompts on images)
- Stealth attacks (subtle, low-contrast text)
- Multiple attack templates and malicious tasks
- Customizable positioning and styling

**Usage:**
```python
from mohammad.attack_image_generator import AttackImageGenerator

generator = AttackImageGenerator()
attacks = generator.generate_attack_set(
    base_images=['path/to/safe.jpg'],
    num_attacks_per_image=2
)
```

**CLI:**
```bash
python mohammad/attack_image_generator.py
```

### `results_analyzer.py`
Analyzes experimental results:
- Logs attack and defense results
- Calculates performance metrics
- Generates summary reports
- Statistical analysis across experiments

**Usage:**
```python
from mohammad.results_analyzer import ResultsAnalyzer

analyzer = ResultsAnalyzer()
analyzer.log_experiment(
    experiment_name="test_1",
    attack_results=attack_data,
    defense_results=defense_data
)
analyzer.print_summary()
```

**CLI:**
```bash
python mohammad/results_analyzer.py
```

## Quick Start

1. **Get Safe Images:**
   ```bash
   python mohammad/dataset_manager.py
   ```

2. **Generate Attack Images:**
   ```bash
   python mohammad/attack_image_generator.py
   ```

3. **Analyze Results:**
   ```bash
   python mohammad/results_analyzer.py
   ```

## Data Structure

```
data/
├── safe_images/
│   ├── train/       # 70% of safe images
│   ├── val/         # 15% of safe images
│   └── test/        # 15% of safe images
└── attack_images/   # Generated attack images

results/             # Experiment results and reports
```

## Dependencies

- PIL/Pillow - Image manipulation
- requests - Downloading images
- Standard library (json, pathlib, statistics)
