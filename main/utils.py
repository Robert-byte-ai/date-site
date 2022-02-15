from PIL import Image
from rembg.bg import remove
import numpy as np
import io
from date_site import settings
from django.db.models.functions import Radians, Cos, Sin, ASin, Sqrt


def add_watermark(image,):
    background = np.fromfile(settings.WATERMARK)
    result = remove(background)
    base_image = Image.open(image)
    watermark = Image.open(io.BytesIO(result)).convert("RGBA")
    watermark.thumbnail((90, 90))
    width, height = base_image.size
    transparent = Image.new('RGBA', (width, height), (0, 0, 0, 0))
    transparent.paste(base_image, (0, 0))
    transparent.paste(watermark, (0, 0), mask=watermark)
    transparent.save(image, format='png')


def distance_1(La1, La2, Lo1, Lo2):
    Lo1 = Radians(Lo1)
    Lo2 = Radians(Lo2)
    La1 = Radians(La1)
    La2 = Radians(La2)
    return 2 * ASin(Sqrt(Sin((La2 - La1) / 2) ** 2 + Cos(La1) * Cos(La2) * Sin((Lo2 - Lo1) / 2) ** 2)) * 6371
