# import torch
# import clip
# from PIL import Image
#
# # Load model once
# device = "cpu"
# model, preprocess = clip.load("ViT-B/32", device=device)
#
# def get_embedding(image_path):
#     print("✅ USING STABLE CLIP")
#
#     image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)
#
#     with torch.no_grad():
#         image_features = model.encode_image(image)
#
#     # Normalize
#     image_features = image_features / image_features.norm(dim=-1, keepdim=True)
#
#     print("TYPE:", type(image_features))
#
#     return image_features

import torch
import clip
from PIL import Image
import numpy as np

device = "cpu"
model, preprocess = clip.load("ViT-B/32", device=device)

def get_embedding(image_path):
    image = preprocess(Image.open(image_path)).unsqueeze(0).to(device)

    with torch.no_grad():
        features = model.encode_image(image)

    features = features / features.norm(dim=-1, keepdim=True)

    embedding = features[0].cpu().numpy()
    embedding = embedding / (np.linalg.norm(embedding) + 1e-10)

    return embedding