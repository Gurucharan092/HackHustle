# def compute_score(sim, hash_dist, ela_flag, exif_flag):
#     score = 100
#     flags = []
#
#     if sim > 0.95:
#         score -= 40
#         flags.append("STOCK_IMAGE_MATCH")
#
#     elif sim > 0.85:
#         score -= 20
#         flags.append("SIMILAR_IMAGE")
#
#     if hash_dist < 5:
#         score -= 30
#         flags.append("DUPLICATE_IMAGE")
#
#     if ela_flag:
#         score -= 20
#         flags.append("EDIT_DETECTED")
#
#     if exif_flag != "OK":
#         score -= 10
#         flags.append("METADATA_MISMATCH")
#
#     return max(score, 0), flags

def compute_score(sim, hash_dist, ela_flag, exif_flag):
    score = 100
    flags = []

    # Similarity
    if sim > 0.95:
        score -= 40
        flags.append("STOCK_IMAGE_MATCH")

    elif sim > 0.85:
        score -= 20
        flags.append("SIMILAR_IMAGE")

    # Hash duplicate
    if hash_dist < 5:
        score -= 25
        flags.append("DUPLICATE_IMAGE")

    # ELA
    if ela_flag:
        score -= 20
        flags.append("POSSIBLE_EDIT")

    # EXIF
    if exif_flag == "OLD":
        score -= 10
        flags.append("OLD_IMAGE_REUSE")

    elif exif_flag == "ERROR":
        flags.append("EXIF_ERROR")

    return max(score, 0), flags