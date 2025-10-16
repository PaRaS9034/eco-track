# classifier_stub.py
# Simple placeholder classifier: replace this with your real ML model later
import random

LABELS = ["plastic", "organic", "metal", "glass", "paper", "unknown"]

def classify_image(image_path):
    """
    Stub function that pretends to classify an image.
    Returns a random label with confidence.
    """
    label = random.choice(LABELS)
    confidence = round(random.uniform(0.6, 0.99), 2)
    return {"label": label, "confidence": confidence}
