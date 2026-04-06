from sentence_transformers import SentenceTransformer
from config.config import config

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(
            config["model"]["embedding"],
            device=config["device"]["type"]
        )
    return _model
