# import pickle
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# from models.clip_model import get_embedding
#
# EMBED_PATH = "data/reference_embeddings.pkl"
#
# with open(EMBED_PATH, "rb") as f:
#     reference_embeddings = pickle.load(f)
#
#
# def _ensure_vector(x):
#     """
#     Ensures embedding is a flat 1D numpy array
#     """
#     if hasattr(x, "detach"):  # torch tensor
#         x = x.detach().cpu().numpy()
#
#     x = np.array(x)
#     x = np.squeeze(x)
#
#     if x.ndim != 1:
#         raise ValueError(f"Invalid embedding shape after squeeze: {x.shape}")
#
#     return x
#
#
# def check_similarity(image_path):
#     """
#     Returns:
#         max_similarity (float)
#         best_match (str)
#     """
#
#     # Get query embedding
#     query_emb = get_embedding(image_path)
#     query_emb = _ensure_vector(query_emb)
#
#     max_sim = -1
#     best_match = None
#
#     for name, emb in reference_embeddings.items():
#         try:
#             emb = _ensure_vector(emb)
#
#             sim = cosine_similarity(
#                 query_emb.reshape(1, -1),
#                 emb.reshape(1, -1)
#             )[0][0]
#
#             if sim > max_sim:
#                 max_sim = sim
#                 best_match = name
#
#         except Exception as e:
#             print(f"⚠️ Skipping {name}: {e}")
#
#     return max_sim, best_match

import pickle
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from models.clip_model import get_embedding

with open("data/reference_embeddings.pkl", "rb") as f:
    ref_embeddings = pickle.load(f)

def check_similarity(image_path):
    query = get_embedding(image_path)

    max_sim = -1
    best_match = None

    for name, emb in ref_embeddings.items():
        sim = cosine_similarity(
            query.reshape(1, -1),
            emb.reshape(1, -1)
        )[0][0]

        if sim > max_sim:
            max_sim = sim
            best_match = name

    return float(max_sim), best_match