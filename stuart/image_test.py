from PIL import Image, ImageFont

text = "Hello world!"
font_size = 36
font_filepath = "Ubuntu-Regular.ttf"
color = (67, 33, 116, 155)

font = ImageFont.truetype(font_filepath, size=font_size)
mask_image = font.getmask(text, "L")
img = Image.new("RGBA", mask_image.size)
img.im.paste(color, (0, 0) + mask_image.size, mask_image)  # need to use the inner `img.im.paste` due to `getmask` returning a core
img.show()