from transformers import pipeline
import os

def download_model():
    cache_dir = "./model_cache"
    os.makedirs(cache_dir, exist_ok=True)
    print("Downloading typeform/distilbert-base-uncased-mnli...")
    classifier = pipeline(
        "zero-shot-classification",
        model="typeform/distilbert-base-uncased-mnli",
        cache_dir=cache_dir
    )
    print("Model downloaded and cached in", cache_dir)

if __name__ == "__main__":
    download_model()