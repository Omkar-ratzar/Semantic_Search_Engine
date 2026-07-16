import numpy as np
from app.core.errors import safe_execution
from app.config.config import config
from app.tasks.embedding.model_loader import get_model
from app.tasks.embedding.normalize import normalize

batch_size = config["batch"]["embedding_batch_size"]
show_progress = config["embedding"]["show_progress"]


@safe_execution(component="EMBEDDING", rethrow=True)
def embed_chunks(texts: list[str]) -> np.ndarray:
    if not texts:
        return np.array([])
    model = get_model()


    vectors = model.encode(
        texts,
        batch_size=batch_size,
        show_progress_bar=show_progress
    )
    return normalize(vectors)
