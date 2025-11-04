#!/usr/bin/env python3
import re
import sys
from PIL import Image
import pytesseract

def ocr_image(path: str) -> str:
    """
    Run OCR on an image and return extracted text.
    """
    img = Image.open(path)
    # Optional preprocessing to improve OCR
    img = img.convert('L')
    text = pytesseract.image_to_string(img)
    return text

def score_text(text: str) -> int:
    """
    Very lightweight heuristic scoring for prompt-injection characteristics.
    Higher score => more suspicious.
    """
    t = text.lower()
    score = 0

    # Password/secret related terms
    if any(w in t for w in ['password', 'passcode', 'credentials', 'secret', 'private', 'token']):
        score += 2

    # Action words often used to exfiltrate or forward prompts
    if any(line for line in t.splitlines() if re.search(r'(forward|send|exfiltrate|deliver|forwarded|forwarding)', line)):
        if any(p in line for line in t.splitlines() for p in ['password', 'secret', 'credential', 'prompt']):
            score += 3

    # Email patterns near sensitive terms (suggests exfiltration)
    if re.search(r'[\w\.-]+@[\w\.-]+', t):
        if re.search(r'(password|secret|credential|prompt|system\s+prompt|internal\s+instruction)', t):
            score += 1

    # Attempts to reveal prompts / internal instructions
    if re.search(r'(system\s+prompt|internal\s+instruction|hidden\s+prompt|ignore\s+instructions|reveal\s+prompt|what\s+can\s+you\s+reveal)', t):
        score += 2

    return score

def detect_prompt_injection(image_path: str, threshold: int = 3):
    """
    Return a dict with extracted text, score, and suspicious flag.
    """
    text = ocr_image(image_path)
    score = score_text(text)
    return {
        'text': text,
        'score': int(score),
        'suspicious': int(score) >= threshold
    }

def main():
    if len(sys.argv) < 2:
        print("Usage: python detect_prompt_injection.py <image_path>")
        sys.exit(1)
    image_path = sys.argv[1]
    result = detect_prompt_injection(image_path)
    print("Suspicious:" , bool(result['suspicious']))
    print("Score     :", result['score'])
    print("Extracted text:\n" + result['text'])

if __name__ == '__main__':
    main()