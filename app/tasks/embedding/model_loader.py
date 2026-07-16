from sentence_transformers import SentenceTransformer
from app.config.config import config
import torch

_model = None

def get_model():
    global _model
    if _model is None:
        _model = SentenceTransformer(
            config["model"]["embedding"],
            local_files_only=True,
            device=config["device"]["type"] if torch.cuda.is_available() else "cpu"
        )
    return _model
