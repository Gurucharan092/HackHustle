# import os
# import imagehash
# from PIL import Image
#
# REF_DIR = "data/reference_images"
#
# # Precompute hashes
# ref_hashes = {}
#
# for file in os.listdir(REF_DIR):
#     path = os.path.join(REF_DIR, file)
#     img = Image.open(path)
#     ref_hashes[file] = imagehash.phash(img)
#
# def check_hash(image_path):
#     query_hash = imagehash.phash(Image.open(image_path))
#
#     min_distance = 100
#
#     for h in ref_hashes.values():
#         dist = query_hash - h
#         if dist < min_distance:
#             min_distance = dist
#
#     return min_distance

import imagehash
from PIL import Image
import os

REFERENCE_FOLDER = "data/reference_images"

def check_hash(image_path):
    try:
        query_hash = imagehash.phash(Image.open(image_path))

        min_dist = 999

        for file in os.listdir(REFERENCE_FOLDER):
            ref_path = os.path.join(REFERENCE_FOLDER, file)

            ref_hash = imagehash.phash(Image.open(ref_path))

            dist = query_hash - ref_hash

            if dist < min_dist:
                min_dist = dist

        return min_dist

    except Exception as e:
        print(f"Hash error: {e}")
        return 999