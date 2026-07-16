from app.tasks.extraction.dispatcher import extract_document
from app.tasks.processing.chunk_text import chunk_text
from app.tasks.embedding.embed_chunks import embed_chunks
from app.tasks.embedding.vector_store import upsert_vectors, init_collection,delete_vectors_by_file_id
from app.core.log import logger,metrics_logger
from app.db.file_repo import mark_processed
from app.config.config import config
from app.core.utils import normalize_path

import uuid
from time import perf_counter

def process_document(file):

    t0 = perf_counter()
    text = extract_document(file["file_path"])
    parsing_time = perf_counter() - t0
    print("FILE:", file["file_path"])
    print("TEXT LEN:", len(text) if text else 0)
    logger.info(f"[SERVICE] Processing {file['file_id']} document")
    if not text:
        logger.error(f"[SERVICE] EXTRACTION FAILED IN document_service.py for {file['file_id']}")
        return
    # return text

    chunk_size = config["chunking"]["chunk_size"]
    overlap = config["chunking"]["overlap"]
    t1 = perf_counter()
    chunks = chunk_text(text, chunk_size, overlap)
    chunking_time = perf_counter() - t1
    if not chunks:
        print(f"[WARN] No chunks: {file['file_path']}")
        return
    t2 = perf_counter()
    vectors = embed_chunks(chunks)
    embedding_time = perf_counter() - t2
    if vectors is None or vectors.shape[0] == 0:
        print(f"[WARN] No vectors for file: {file['file_path']}")
        return

    init_collection(dim=len(vectors[0]))

    ids = []
    payloads = []

    for i, chunk in enumerate(chunks):
        ids.append(str(uuid.uuid5(uuid.NAMESPACE_DNS, f"{file['file_id']}_{i}")))
        payloads.append({
            "file_id": file["file_id"],
            "file_name": file["file_path"],
            "text": chunk
        })
    if not ids:
        logger.error(f"No valid IDs/chunks for file {file['file_id']}, skipping delete/upsert")
        return
    try:
        t3 = perf_counter()
        delete_vectors_by_file_id(file["file_id"])
        upsert_vectors(ids, vectors, payloads)
        indexing_time = perf_counter() - t3
        pipeline_time = perf_counter() - t0
        num_chunks = len(chunks)
        num_embeddings = len(vectors)
        embeddings_per_sec = num_embeddings / embedding_time
        chunks_per_sec = num_chunks / chunking_time
        text_size = len(text)
        avg_chunk_length = sum(len(c) for c in chunks) / len(chunks)
        vector_dimension = vectors.shape[1]
        import json

        metrics_logger.info(json.dumps({
            "file_id": file["file_id"],
            "text_len":text_size,
            "parsing_ms": parsing_time * 1000,
            "chunking_ms": chunking_time * 1000,
            "embedding_ms": embedding_time * 1000,
            "indexing_ms": indexing_time * 1000,
            "pipeline_ms": pipeline_time * 1000,
            "chunks": num_chunks,
            "chunks_per_sec": chunks_per_sec,
            "avg_chunk_len":avg_chunk_length,
            "embeddings": num_embeddings,
            "embeddings_per_sec": embeddings_per_sec,
            "vector_dim":vector_dimension
        }))
        mark_processed(file["file_path"])

    except Exception as e:
        logger.error(f"Vector upsert failed for {file['file_id']}: {e}")
        raise
