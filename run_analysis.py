# import os
#
# from services.similarity import check_similarity
# from services.hashing import check_hash
# from services.ela import detect_ela
# from services.exif import check_exif
# from services.scoring import compute_score
#
# DATASET_DIR = "data/generated_dataset"
#
# def analyze_image(path):
#     sim, match = check_similarity(path)   # ✅ FIX
#     hash_dist = check_hash(path)
#     ela_flag = detect_ela(path)
#     exif_flag = check_exif(path)
#
#     score, flags = compute_score(sim, hash_dist, ela_flag, exif_flag)
#
#     return {
#         "score": score,
#         "flags": flags,
#         "similarity": sim,
#         "best_match": match,
#         "hash_distance": hash_dist,
#         "ela": ela_flag,
#         "exif": exif_flag
#     }
#
# print("\n🚀 Running Vision Fraud Detection\n")
#
# # 🔴 DEBUG: check folder exists
# if not os.path.exists(DATASET_DIR):
#     print(f"❌ Folder not found: {DATASET_DIR}")
#     exit()
#
# files = os.listdir(DATASET_DIR)
#
# # 🔴 DEBUG: print files
# print(f"📂 Found {len(files)} files in dataset")
#
# valid_images = [f for f in files if f.lower().endswith((".jpg", ".jpeg", ".png"))]
#
# print(f"🖼️ Valid images: {len(valid_images)}")
#
# if len(valid_images) == 0:
#     print("❌ No valid images found. Check extensions.")
#     exit()
#
# # 🔥 MAIN LOOP
# for file in valid_images:
#     path = os.path.join(DATASET_DIR, file)
#
#     print(f"\n🔍 Processing: {file}")
#
#     try:
#         result = analyze_image(path)
#
#         print(f"Score: {result['score']}")
#         print(f"Flags: {result['flags']}")
#         print(f"Similarity: {result['similarity']:.3f}")
#         print(f"Hash Distance: {result['hash_distance']}")
#         print(f"ELA: {result['ela']}")
#         print(f"EXIF: {result['exif']}")
#
#     except Exception as e:
#         print(f"❌ Error processing {file}: {e}")

import os
import pickle
from PIL import Image

from models.clip_model import get_embedding
from services.similarity import find_top_k_similar
from services.ela import detect_ela
from services.exif import check_exif
import imagehash

DATASET_PATH = "data/generated_dataset"
EMBEDDINGS_PATH = "data/reference_embeddings.pkl"


# -------------------------------
# Load embeddings
# -------------------------------
with open(EMBEDDINGS_PATH, "rb") as f:
    db_embeddings = pickle.load(f)


# -------------------------------
# Fraud decision logic
# -------------------------------
def fraud_decision(score):
    if score >= 80:
        return "APPROVE ✅"
    elif 50 <= score < 80:
        return "REVIEW ⚠️"
    else:
        return "REJECT 🚫"


# -------------------------------
# Score calculation
# -------------------------------
def compute_score(similarity, hash_distance, ela_flag, exif_status):
    score = 100

    # Similarity penalties
    if similarity > 0.95:
        score -= 60
    elif similarity > 0.85:
        score -= 40
    elif similarity > 0.75:
        score -= 20

    # Duplicate detection
    if hash_distance == 0:
        score -= 25
    elif hash_distance < 5:
        score -= 15

    # ELA (editing)
    if ela_flag:
        score -= 20

    # Metadata issues
    if exif_status != "VALID":
        score -= 10

    return max(score, 0)


# -------------------------------
# Flag generator
# -------------------------------
def generate_flags(similarity, hash_distance, ela_flag, exif_status):
    flags = []

    if similarity > 0.95:
        flags.append("STOCK_IMAGE_MATCH")
    elif similarity > 0.85:
        flags.append("SIMILAR_IMAGE")

    if hash_distance == 0:
        flags.append("DUPLICATE_IMAGE")

    if ela_flag:
        flags.append("POSSIBLE_EDIT")

    if exif_status != "VALID":
        flags.append("METADATA_MISSING")

    return flags


# -------------------------------
# Run analysis
# -------------------------------
def run():
    print("\n🚀 Running Vision Fraud Detection\n")

    files = [f for f in os.listdir(DATASET_PATH) if f.lower().endswith((".jpg", ".png"))]

    print(f"📂 Found {len(files)} files in dataset\n")

    for file in files:
        try:
            path = os.path.join(DATASET_PATH, file)

            print("🔍 Processing:", file)

            # -------------------
            # Embedding
            # -------------------
            emb = get_embedding(path)

            # -------------------
            # Similarity (Top 3)
            # -------------------
            top_matches = find_top_k_similar(emb, db_embeddings, k=3)
            best_match, best_similarity = top_matches[0]

            # -------------------
            # Hash comparison
            # -------------------
            img = Image.open(path)
            query_hash = imagehash.phash(img)

            best_hash = imagehash.phash(Image.open(os.path.join("data/reference_images", best_match)))
            hash_distance = query_hash - best_hash

            # -------------------
            # ELA
            # -------------------
            ela_flag = detect_ela(path)

            # -------------------
            # EXIF
            # -------------------
            exif_status = check_exif(path)

            # -------------------
            # Score + Flags
            # -------------------
            score = compute_score(best_similarity, hash_distance, ela_flag, exif_status)
            flags = generate_flags(best_similarity, hash_distance, ela_flag, exif_status)
            decision = fraud_decision(score)

            # -------------------
            # OUTPUT
            # -------------------
            print(f"\n🧠 Decision: {decision}")
            print(f"📊 Score: {score}")
            print(f"🚩 Flags: {flags}")

            print("\n🔎 Top Similar Images:")
            for name, sim in top_matches:
                print(f"   → {name} (Similarity: {round(sim, 3)})")

            print("\n📌 Signals:")
            print(f"   Similarity: {round(best_similarity, 3)}")
            print(f"   Hash Distance: {hash_distance}")
            print(f"   ELA Manipulation: {ela_flag}")
            print(f"   EXIF Status: {exif_status}")

            print("\n🧾 Explanation:")
            if "STOCK_IMAGE_MATCH" in flags:
                print("   Image matches known product/stock image.")
            elif "SIMILAR_IMAGE" in flags:
                print("   Image is highly similar to existing images.")
            if "DUPLICATE_IMAGE" in flags:
                print("   Exact duplicate detected.")
            if "POSSIBLE_EDIT" in flags:
                print("   Signs of image editing detected.")
            if exif_status != "VALID":
                print("   Metadata missing or inconsistent.")

            print("\n" + "-" * 60 + "\n")

        except Exception as e:
            print(f"❌ Error processing {file}: {e}")


# -------------------------------
# ENTRY
# -------------------------------
if __name__ == "__main__":
    run()
# import os
# from services.similarity import check_similarity
# from services.hashing import check_hash
# from services.ela import detect_ela
# from services.exif import check_exif
# from services.scoring import compute_score

# DATASET = "data/generated_dataset"


# def analyze_image(path):
#     sim, match = check_similarity(path)
#     hash_dist = check_hash(path)
#     ela_flag = detect_ela(path)
#     exif_flag = check_exif(path)

#     score, flags = compute_score(sim, hash_dist, ela_flag, exif_flag)

#     print(f"\n🔍 Processing: {os.path.basename(path)}")
#     print(f"Score: {score}")
#     print(f"Flags: {flags}")
#     print(f"Similarity: {round(sim,3)}")
#     print(f"Best Match: {match}")
#     print(f"Hash Distance: {hash_dist}")
#     print(f"ELA: {ela_flag}")
#     print(f"EXIF: {exif_flag}")


# def main():
#     print("\n🚀 Running Vision Fraud Detection\n")

#     files = os.listdir(DATASET)
#     print(f"📂 Found {len(files)} files in dataset")

#     for file in files:
#         path = os.path.join(DATASET, file)

#         try:
#             analyze_image(path)
#         except Exception as e:
#             print(f"❌ Error processing {file}: {e}")


# if __name__ == "__main__":
#     main()