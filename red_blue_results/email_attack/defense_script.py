from PIL import Image
import pytesseract
import re

def detect_attack(image_path):
    """
    Detects potential prompt injection attacks in an image.

    Args:
        image_path: The path to the image file.

    Returns:
        True if a potential attack is detected, False otherwise.
    """
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)

        # Check for common prompt injection keywords and phrases
        keywords = ["forward", "password", "prompt", "insert", "override", "execute", "command", "system", "shell"]
        for keyword in keywords:
            if keyword in text.lower():
                return True

        # Check for unusual formatting or patterns
        if "VERY IMPORTANT" in text:
            return True

        return False

    except Exception as e:
        print(f"Error processing image: {e}")
        return False

if __name__ == \'__main__\':
    # Replace \'image.png\' with the actual path to your image file
    image_path = \'image.png