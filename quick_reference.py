"""
Quick Reference for Running the Project Components
"""

# ============================================================
# SETUP (Run once)
# ============================================================

# Install all dependencies
# pip install -r requirements.txt

# ============================================================
# TESTING YOUR COMPONENTS
# ============================================================

# 1. Test Attack Success Detector
from aadarsha.attack_success_detector import AttackSuccessDetector

detector = AttackSuccessDetector()
vlm_response = "Sure! Here is how to hack the system..."
result = detector.check_success(vlm_response)
print(f"Attack succeeded: {result['success']}")

# 2. Test Defense Validator
from aadarsha.defense_validator import DefenseValidator

validator = DefenseValidator()
# When you have images and defense scripts ready:
# results = validator.validate_defense(
#     "path/to/defense_script.py",
#     ["attack1.png", "attack2.png"],
#     ["safe1.png", "safe2.png"]
# )
# validator.print_results(results)

# ============================================================
# FULL INTEGRATION TEST
# ============================================================

# Run this to see everything working together
# python test_integration.py

# ============================================================
# EXAMPLE: Create a Mock Defense Script to Test
# ============================================================

# Save this as example_defense.py to test the validator:
"""
def detect_attack(image_path):
    # Mock defense: checks if filename contains 'attack'
    return 'attack' in image_path.lower()
"""

# Then test it:
# results = validator.validate_defense(
#     "example_defense.py",
#     ["test_attack_1.png"],
#     ["test_safe_1.png"]
# )

# ============================================================
# CONNECTING TO A REAL VLM
# ============================================================

# OpenAI GPT-4V example (you'll need an API key)
"""
from openai import OpenAI
import base64

def query_vlm(image_path, prompt):
    client = OpenAI(api_key="your-api-key")
    
    with open(image_path, "rb") as img:
        base64_image = base64.b64encode(img.read()).decode()
    
    response = client.chat.completions.create(
        model="gpt-4-vision-preview",
        messages=[{
            "role": "user",
            "content": [
                {"type": "text", "text": prompt},
                {"type": "image_url", "image_url": {"url": f"data:image/png;base64,{base64_image}"}}
            ]
        }]
    )
    
    return response.choices[0].message.content

# Use it with your detector
vlm_response = query_vlm("attack.png", "Describe this image")
result = detector.check_success(vlm_response)
"""
