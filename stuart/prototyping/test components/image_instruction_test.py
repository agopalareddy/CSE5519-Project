from PIL import Image, ImageFont
import base64
from io import BytesIO
from transformers import pipeline

text = "What is 5 times 5?"
font_size = 36
font_filepath = "Ubuntu-Regular.ttf"
color = (67, 33, 116, 155)

font = ImageFont.truetype(font_filepath, size=font_size)
mask_image = font.getmask(text, "L")
img = Image.new("RGBA", mask_image.size)
img.im.paste(color, (0, 0) + mask_image.size, mask_image)  # need to use the inner `img.im.paste` due to `getmask` returning a core

pipe = pipeline("image-text-to-text", model="google/gemma-3-4b-it")

messages = [
    {
        "role": "user",
        "content": [
            {"type": "image"},
            {"type": "text", "text": ""},
        ],
    }
]

outputs = pipe(text=messages, images=[img])
result = outputs[0]["generated_text"]

print(result)