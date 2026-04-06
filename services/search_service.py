from tasks.embedding.embed_chunks import embed_chunks
from tasks.embedding.vector_store import search

def search_query(query, top_k=5):
    vector = embed_chunks([query])[0]
    results = search(vector, top_k)

    return [
        {
            "score": r.score,
            "file": r.payload.get("file_name"),
            # "text": r.payload.get("text")
        }
        for r in results
    ]
