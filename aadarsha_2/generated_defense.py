"""OCR-based prompt injection detection."""
import os

# Keywords to detect potential attacks
ATTACK_KEYWORDS = ['ignore', 'disregard', 'forget', 'override', 'instead', 'instructions', 'actually', 'forward', 'send', 'email', 'password', 'secret']

def extract_text_from_image(image_path):
    """Extract text from image using available OCR method."""
    try:
        # Try using pytesseract (requires tesseract installed)
        import pytesseract
        from PIL import Image
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img)
        return text.lower()
    except ImportError:
        pass
    except Exception as e:
        pass
    
    try:
        # Fallback: try easyocr
        import easyocr
        reader = easyocr.Reader(["en"], gpu=False, verbose=False)
        results = reader.readtext(image_path)
        text = " ".join([r[1] for r in results])
        return text.lower()
    except ImportError:
        pass
    except Exception as e:
        pass
    
    # If no OCR available, return empty string (won't detect anything)
    return ""

def detect_attack(image_path):
    """
    Detect if an image contains a prompt injection attack.
    
    Args:
        image_path: Path to the image file
        
    Returns:
        True if attack detected, False otherwise
    """
    if not os.path.exists(image_path):
        return False
    
    # Extract text from image
    image_text = extract_text_from_image(image_path)
    
    if not image_text:
        # No text found in image - likely a benign image
        return False
    
    # Count how many attack keywords are found
    keywords_found = 0
    for keyword in ATTACK_KEYWORDS:
        if keyword in image_text:
            keywords_found += 1
    
    # Also check for suspicious patterns (text that looks like instructions)
    suspicious_patterns = [
        "ignore", "disregard", "forget", "instead", "override",
        "new instruction", "follow these", "do not", "don't",
        "send to", "forward to", "password", "secret", "confidential"
    ]
    pattern_matches = sum(1 for p in suspicious_patterns if p in image_text)
    
    # Flag as attack if:
    # 1. At least 1 keyword found AND some text present (>20 chars suggests instruction text)
    # 2. OR at least 1 suspicious pattern found
    # 3. OR at least 2 keywords found
    has_substantial_text = len(image_text.strip()) > 20
    
    if keywords_found >= 2:
        return True
    if keywords_found >= 1 and has_substantial_text:
        return True
    if pattern_matches >= 1:
        return True
    
    return False
