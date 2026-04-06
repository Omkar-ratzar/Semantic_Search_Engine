from core.errors import safe_execution
from core.log import logger
from config.config import config

chunk_size= config["chunking"]["chunk_size"]
overlap= config["chunking"]["overlap"]


def chunk_text(text, chunk_size=chunk_size, overlap=overlap):
    words = text.split()

    if not words:
        return []

    step = chunk_size - overlap

    if step <= 0:
        raise ValueError(
            f"Invalid config: chunk_size ({chunk_size}) must be > overlap ({overlap})"
        )

    chunks = []

    for i in range(0, len(words), step):
        chunk = " ".join(words[i:i + chunk_size])
        if chunk.strip():
            chunks.append(chunk)

    return chunks
