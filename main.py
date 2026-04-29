import os
import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageEnhance
import random
import shutil

INPUT_DIR = "data/reference_images"
OUTPUT_DIR = "data/generated_dataset"

os.makedirs(OUTPUT_DIR, exist_ok=True)


def load_image(path):
    return Image.open(path).convert("RGB")


def save(img, path):
    img.save(path, "JPEG", quality=95)


# 1. Genuine
def genuine(img, name):
    save(img, f"{OUTPUT_DIR}/{name}_genuine.jpg")


# 2. Exact reuse
def reuse(img, name):
    save(img, f"{OUTPUT_DIR}/{name}_reuse.jpg")


# 3. Cropped
def cropped(img, name):
    w, h = img.size
    crop = img.crop((w * 0.1, h * 0.1, w * 0.9, h * 0.9))
    save(crop, f"{OUTPUT_DIR}/{name}_cropped.jpg")


# 4. Rotated
def rotated(img, name):
    rot = img.rotate(15)
    save(rot, f"{OUTPUT_DIR}/{name}_rotated.jpg")


# 5. Fake crack (draw lines)
def fake_crack(img, name):
    crack = img.copy()
    draw = ImageDraw.Draw(crack)
    for _ in range(5):
        x1, y1 = random.randint(0, img.width), random.randint(0, img.height)
        x2, y2 = random.randint(0, img.width), random.randint(0, img.height)
        draw.line((x1, y1, x2, y2), fill=(255, 255, 255), width=2)
    save(crack, f"{OUTPUT_DIR}/{name}_fake_edit.jpg")


# 6. Screenshot-like (resize + compress)
def screenshot(img, name):
    small = img.resize((int(img.width * 0.6), int(img.height * 0.6)))
    save(small, f"{OUTPUT_DIR}/{name}_screenshot.jpg")


# 7. Recompressed multiple times
def recompress(img, name):
    temp = img
    for i in range(3):
        temp_path = f"{OUTPUT_DIR}/temp_{i}.jpg"
        temp.save(temp_path, quality=50)
        temp = Image.open(temp_path)
    save(temp, f"{OUTPUT_DIR}/{name}_recompressed.jpg")


# 8. Metadata stripped
def strip_metadata(img, name):
    data = list(img.getdata())
    clean = Image.new(img.mode, img.size)
    clean.putdata(data)
    save(clean, f"{OUTPUT_DIR}/{name}_no_metadata.jpg")


# 9. Blur + noise
def blur_noise(img, name):
    arr = np.array(img)
    noise = np.random.randint(0, 50, arr.shape, dtype='uint8')
    noisy = cv2.add(arr, noise)
    blurred = cv2.GaussianBlur(noisy, (5, 5), 0)
    out = Image.fromarray(blurred)
    save(out, f"{OUTPUT_DIR}/{name}_blur_noise.jpg")


# 10. Copy-paste tampering
def copy_paste(img, name):
    cp = img.copy()
    w, h = img.size
    region = cp.crop((0, 0, w // 3, h // 3))
    cp.paste(region, (w // 2, h // 2))
    save(cp, f"{OUTPUT_DIR}/{name}_copy_paste.jpg")


# 11. Clean (no damage)
def clean_image(name):
    clean = Image.new("RGB", (512, 512), color=(200, 200, 200))
    save(clean, f"{OUTPUT_DIR}/{name}_clean.jpg")


# 12. Mixed fraud case
def mixed_case(img, name):
    mixed = img.copy()

    # add crack
    draw = ImageDraw.Draw(mixed)
    for _ in range(3):
        draw.line(
            (random.randint(0, mixed.width), random.randint(0, mixed.height),
             random.randint(0, mixed.width), random.randint(0, mixed.height)),
            fill=(255, 255, 255), width=2
        )

    # blur + compress
    arr = np.array(mixed)
    arr = cv2.GaussianBlur(arr, (7, 7), 0)
    mixed = Image.fromarray(arr)

    save(mixed, f"{OUTPUT_DIR}/{name}_mixed.jpg")


# MAIN LOOP
for file in os.listdir(INPUT_DIR):
    if file.lower().endswith((".jpg", ".png", ".jpeg")):
        path = os.path.join(INPUT_DIR, file)
        name = os.path.splitext(file)[0]
        img = load_image(path)

        genuine(img, name)
        reuse(img, name)
        cropped(img, name)
        rotated(img, name)
        fake_crack(img, name)
        screenshot(img, name)
        recompress(img, name)
        strip_metadata(img, name)
        blur_noise(img, name)
        copy_paste(img, name)
        mixed_case(img, name)

# create clean example separately
clean_image("sample")

print("✅ All 12 scenarios generated in /generated_dataset")