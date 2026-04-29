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
from services.similarity import check_similarity
from services.hashing import check_hash
from services.ela import detect_ela
from services.exif import check_exif
from services.scoring import compute_score

DATASET = "data/generated_dataset"


def analyze_image(path):
    sim, match = check_similarity(path)
    hash_dist = check_hash(path)
    ela_flag = detect_ela(path)
    exif_flag = check_exif(path)

    score, flags = compute_score(sim, hash_dist, ela_flag, exif_flag)

    print(f"\n🔍 Processing: {os.path.basename(path)}")
    print(f"Score: {score}")
    print(f"Flags: {flags}")
    print(f"Similarity: {round(sim,3)}")
    print(f"Best Match: {match}")
    print(f"Hash Distance: {hash_dist}")
    print(f"ELA: {ela_flag}")
    print(f"EXIF: {exif_flag}")


def main():
    print("\n🚀 Running Vision Fraud Detection\n")

    files = os.listdir(DATASET)
    print(f"📂 Found {len(files)} files in dataset")

    for file in files:
        path = os.path.join(DATASET, file)

        try:
            analyze_image(path)
        except Exception as e:
            print(f"❌ Error processing {file}: {e}")


if __name__ == "__main__":
    main()