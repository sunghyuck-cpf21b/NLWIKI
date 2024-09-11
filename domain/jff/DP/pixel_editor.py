from PIL import Image


def hex_to_rgb(hex):
    return tuple(int(hex[i:i+2], 16) for i in (0, 2, 4))

def image_editor(x, y, color, name: str):
    image = Image.open(name)
    pixel = image.load()
    pixel[x, y] = hex_to_rgb(color)
    image.save(name)