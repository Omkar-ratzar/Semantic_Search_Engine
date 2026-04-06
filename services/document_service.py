from tasks.extraction.dispatcher import extract_document
from tasks.processing.chunk_text import chunk_text
from tasks.embedding.embed_chunks import embed_chunks
from tasks.embedding.vector_store import upsert_vectors, init_collection
from core.log import logger
from config.config import config
import uuid

def process_document(file):
    text = extract_document(file["file_path"])
    print("FILE:", file["file_path"])
    print("TEXT LEN:", len(text) if text else 0)
    logger.info(f"[SERVICE] Processing {file['file_id']} document")
    if not text:
        logger.error(f"[SERVICE] EXTRACTION FAILED IN document_service.py for {file['file_id']}")
        return


    chunk_size = config["chunking"]["chunk_size"]
    overlap = config["chunking"]["overlap"]

    chunks = chunk_text(text, chunk_size, overlap)
    if not chunks:
        print(f"[WARN] No chunks: {file['file_path']}")
        return
    vectors = embed_chunks(chunks)

    if vectors is None or vectors.shape[0] == 0:
        print(f"[WARN] No vectors for file: {file['file_path']}")
        return

    init_collection(dim=len(vectors[0]))

    ids = []
    payloads = []

    for i, chunk in enumerate(chunks):
        ids.append(str(uuid.uuid4()))
        payloads.append({
            "file_id": file["file_id"],
            "file_name": file["file_path"],
            "text": chunk
        })

    upsert_vectors(ids, vectors, payloads)
