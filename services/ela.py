# from PIL import Image, ImageChops, ImageEnhance
# import numpy as np
#
# def detect_ela(image_path, threshold=10):
#     original = Image.open(image_path).convert("RGB")
#
#     # Save at lower quality
#     temp_path = "temp_ela.jpg"
#     original.save(temp_path, "JPEG", quality=90)
#
#     compressed = Image.open(temp_path)
#
#     ela = ImageChops.difference(original, compressed)
#     enhancer = ImageEnhance.Brightness(ela)
#     ela = enhancer.enhance(10)
#
#     ela_np = np.array(ela)
#
#     # Mean intensity check
#     mean_val = ela_np.mean()
#
#     return mean_val > threshold

from PIL import Image, ImageChops, ImageEnhance
import numpy as np

def detect_ela(image_path, threshold=25):
    try:
        original = Image.open(image_path).convert("RGB")
        temp_path = "temp_ela.jpg"

        original.save(temp_path, "JPEG", quality=90)
        compressed = Image.open(temp_path)

        diff = ImageChops.difference(original, compressed)
        diff = ImageEnhance.Brightness(diff).enhance(5)

        diff_np = np.array(diff)

        mean_diff = diff_np.mean()

        return mean_diff > threshold

    except:
        return False