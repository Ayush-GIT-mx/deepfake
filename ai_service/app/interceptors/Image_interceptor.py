import numpy as np
from PIL import Image
import exifread

# ------------------ Loaders ------------------

def load_image(path: str) -> Image.Image:
    """Load an image from a given file path."""
    return Image.open(path)

def get_exif_data(path: str) -> dict:
    """Extract EXIF metadata from an image file."""
    try:
        with open(path, 'rb') as f:
            tags = exifread.process_file(f, details=False)
        return {tag: str(tags[tag]) for tag in tags}
    except Exception:
        return {}

# ------------------ Checks ------------------

def check_metadata(exif: dict, filename: str = "") -> tuple[int, list[str]]:
    suspicious_tags = ['Software', 'Image Description']
    missing_camera_tags = ['Make', 'Model']
    reasons = []
    score = 0

    # Case 1: No EXIF at all
    if not exif:
        score = 1
        reasons.append("No EXIF metadata (likely AI-generated)")
        return score, reasons

    # Case 2: Suspicious EXIF conditions
    if exif.get("EXIF LightSource", "").lower() == "unknown" and exif.get("Image Orientation", "0") == "0":
        score = 1
        reasons.append("Suspicious EXIF (LightSource=Unknown, Orientation=0)")

    # Case 3: Software tags mentioning AI tools
    for tag in suspicious_tags:
        if tag in exif and any(ai in exif[tag].lower() for ai in ["ai", "dall", "meta", "stable", "midjourney"]):
            score = 1
            reasons.append(f"Suspicious EXIF tag: {tag} = {exif[tag]}")

    # Case 4: Missing essential camera info
    if any(tag not in exif for tag in missing_camera_tags):
        score = 1
        reasons.append("Missing essential camera tags (Make/Model)")

    # Case 5: File name hints
    if any(ai in filename.lower() for ai in ["meta", "dalle", "ai", "stable", "mj"]):
        score = 1
        reasons.append("Filename suggests AI origin")

    return score, reasons

def check_entropy(image: Image.Image) -> float:
    grayscale = image.convert('L')
    pixels = np.array(grayscale).flatten()
    histogram = np.histogram(pixels, bins=256)[0]
    probs = histogram / np.sum(histogram)
    entropy = -np.sum([p * np.log2(p) for p in probs if p > 0])
    return float(entropy)

def check_color_distribution(image: Image.Image) -> float:
    pixels = np.array(image)
    if len(pixels.shape) == 3:  # RGB
        r, g, b = pixels[:, :, 0], pixels[:, :, 1], pixels[:, :, 2]
        return float(np.mean([np.std(r), np.std(g), np.std(b)]))
    return 0.0

def check_blockiness(image: Image.Image) -> float:
    grayscale = image.convert('L')
    pixels = np.array(grayscale)
    h, w = pixels.shape
    blocks = []
    for i in range(0, h - 8, 8):
        for j in range(0, w - 8, 8):
            block = pixels[i:i + 8, j:j + 8]
            blocks.append(np.std(block))
    return float(np.mean(blocks)) if blocks else 0.0

# ------------------ Main Inspector ------------------

def image_inspector(path: str) -> dict:
    """Run AI vs Human heuristic detection on an image file."""
    image = load_image(path)
    exif = get_exif_data(path)

    flags = []
    metrics = {}

    # --- Run checks ---
    meta_score, meta_reasons = check_metadata(exif, path)
    entropy = check_entropy(image)
    color_std = check_color_distribution(image)
    blockiness = check_blockiness(image)

    metrics.update({
        "entropy": round(entropy, 2),
        "color_std": round(color_std, 2),
        "blockiness": round(blockiness, 2),
        "metadata_score": meta_score
    })

    # --- Immediate AI verdict if suspicious EXIF ---
    if meta_score > 0:
        flags.extend(meta_reasons)
        return {
            "verdict": "Likely AI-generated",
            "confidence": 1.0,
            "flags": flags,
            "metrics": metrics,
            "exif": exif
        }

    # --- Weighted Scoring ---
    weights = {
        "metadata": 0.25,
        "entropy": 0.25,
        "color_std": 0.25,
        "blockiness": 0.25
    }

    score = 0.0

    # Entropy check
    if entropy < 5.0:
        score += weights["entropy"]
        flags.append("Low entropy (possible synthetic texture)")

    # Color distribution check
    if color_std < 20:
        score += weights["color_std"]
        flags.append("Low color variation (possible AI palette)")

    # Blockiness check (skip for PNG images)
    if image.format != "PNG" and blockiness < 5:
        score += weights["blockiness"]
        flags.append("Low JPEG blockiness (may lack natural compression)")

    final_verdict = "Likely AI-generated" if score > 0.5 else "Likely Human-captured"

    return {
        "verdict": final_verdict,
        "confidence": round(score, 2),
        "flags": flags,
        "metrics": metrics,
        "exif": exif
    }