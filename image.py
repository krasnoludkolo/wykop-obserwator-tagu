import io

from PIL import Image
import requests

from config import ImageConverterConfig


# based on https://pythoncircle.com/post/674/python-script-13-generating-ascii-code-from-image/
class ImageConverter:
    def __init__(self, config: ImageConverterConfig):
        self.config = config

    def convert_to_ascii(self, image_url: str) -> str:
        r = requests.get(image_url)
        img = Image.open(io.BytesIO(r.content))
        width, height = img.size
        aspect_ratio = height / width
        new_width = self.config.img_width
        new_height = aspect_ratio * new_width * 0.55
        img = img.resize((new_width, int(new_height)))

        img = img.convert('L')

        pixels = img.getdata()

        chars = ["B", "S", "#", "&", "@", "$", "%", "*", "!", ":", "."]
        new_pixels = [chars[pixel // 25] for pixel in pixels]
        new_pixels = ''.join(new_pixels)

        new_pixels_count = len(new_pixels)
        ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
        ascii_image = "\n".join(ascii_image)
        return ascii_image
