import numpy as np

def cosine_similarity(a, b):
    a = a.flatten()
    b = b.flatten()
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))


def find_top_k_similar(query_emb, db_embeddings, k=3):
    scores = []

    for name, emb in db_embeddings.items():
        sim = cosine_similarity(query_emb, emb)
        scores.append((name, sim))

    # Sort by similarity descending
    scores.sort(key=lambda x: x[1], reverse=True)

    return scores[:k]  # Top K matches

# import pickle
# import numpy as np
# from sklearn.metrics.pairwise import cosine_similarity
# from models.clip_model import get_embedding

# with open("data/reference_embeddings.pkl", "rb") as f:
#     ref_embeddings = pickle.load(f)

# def check_similarity(image_path):
#     query = get_embedding(image_path)

#     max_sim = -1
#     best_match = None

#     for name, emb in ref_embeddings.items():
#         sim = cosine_similarity(
#             query.reshape(1, -1),
#             emb.reshape(1, -1)
#         )[0][0]

#         if sim > max_sim:
#             max_sim = sim
#             best_match = name

    return float(max_sim), best_match