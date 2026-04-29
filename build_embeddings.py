# import os
# import pickle
# from models.clip_model import get_embedding
#
# REF_DIR = "data/reference_images"
# OUT_PATH = "data/reference_embeddings.pkl"
#
# embeddings = {}
#
# for file in os.listdir(REF_DIR):
#     path = os.path.join(REF_DIR, file)
#     embeddings[file] = get_embedding(path)
#
# with open(OUT_PATH, "wb") as f:
#     pickle.dump(embeddings, f)
#
# print("✅ Embeddings saved")

import os
import pickle
from models.clip_model import get_embedding

folder = "data/reference_images"
embeddings = {}

for file in os.listdir(folder):
    path = os.path.join(folder, file)

    try:
        embeddings[file] = get_embedding(path)
    except Exception as e:
        print(f"Skipping {file}: {e}")

with open("data/reference_embeddings.pkl", "wb") as f:
    pickle.dump(embeddings, f)

print("✅ Embeddings saved")