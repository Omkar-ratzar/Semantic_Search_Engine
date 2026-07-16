from app.tasks.embedding.embed_chunks import embed_chunks
from app.tasks.embedding.vector_store import search
from app.core.log import logger,metrics_logger
# from datetime import datetime
import time
import os

def search_query(query, top_k=15):
    t0 = time.perf_counter()
    vector = embed_chunks([query])[0]
    t1 = time.perf_counter()
    results = search(vector, top_k)
    t2 = time.perf_counter()

    formatted_result= [
        {
            "score": r.score,
            "file": r.payload.get("file_name"),
            # "text": r.payload.get("text")
        }
        for r in results
    ]
    t3 = time.perf_counter()
    import json
    print(metrics_logger)
    print(metrics_logger.handlers)
    print(metrics_logger.level)
    print(metrics_logger.propagate)
    metrics_logger.info(json.dumps({
        "LOG_TYPE":"Search",
        "query_length": len(query),
        "embedding_ms": round((t1 - t0) * 1000, 2),
        "vector_search_ms": round((t2 - t1) * 1000, 2),
        "formatting_ms": round((t3 - t2) * 1000, 2),
        "total_ms": round((t3 - t0) * 1000, 2),
        "top_k":top_k,
        "returned":len(formatted_result)
    }))
    print(f"{top_k} {len(query)} {round((t1 - t0) * 1000, 2)} LOGGED??")
    return {"results":formatted_result,
        "metrics": {
            "embedding_ms": round((t1 - t0) * 1000, 2),
            "vector_search_ms": round((t2 - t1) * 1000, 2),
            "formatting_ms": round((t3 - t2) * 1000, 2),
            "total_ms": round((t3 - t0) * 1000, 2),
            "top_k":top_k,
            "returned":len(formatted_result)
        }
        }
