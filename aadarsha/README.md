# Aadarsha's Project Components

This directory contains the modules I'm responsible for building.

## Files

### `attack_success_detector.py`
Determines if a red team attack successfully jailbroke the target VLM.
- Analyzes VLM responses for compliance vs refusal patterns
- Returns success/failure with confidence scores

### `defense_validator.py`
Tests blue team defense scripts against images.
- Loads Python detection scripts dynamically
- Calculates precision, recall, and accuracy
- Tests against both malicious and benign images

## Next Steps

1. **Test with Stuart's attack examples** - Once Stuart has working attacks, integrate them
2. **Coordinate with Mohammad** - Get the safe image dataset to test defenses
3. **Refine success detection** - May need more sophisticated NLP or VLM-based analysis
4. **Build integration pipeline** - Connect these modules to the red-blue loop

## Dependencies

```bash
# Install required packages
pip install pillow opencv-python
```

## Usage Examples

See the `if __name__ == "__main__"` blocks in each file for basic usage.
