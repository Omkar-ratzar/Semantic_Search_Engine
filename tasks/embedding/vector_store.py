from qdrant_client import QdrantClient
from qdrant_client.models import VectorParams, Distance, PointStruct
from config.config import config
import uuid
COLLECTION_NAME = "documents"

client = QdrantClient(host="localhost", port=6333)


def init_collection(dim: int):
    if COLLECTION_NAME in [c.name for c in client.get_collections().collections]:
        return

    client.create_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=VectorParams(size=dim, distance=Distance.COSINE),
    )


def upsert_vectors(ids, vectors, payloads):
    points = [
        PointStruct(id=i, vector=v.tolist(), payload=p)
        for i, v, p in zip(ids, vectors, payloads)
    ]

    client.upsert(
        collection_name=COLLECTION_NAME,
        points=points
    )

def search(query_vector, top_k=5):
    results = client.query_points(
        collection_name=COLLECTION_NAME,
        query=query_vector.tolist(),
        limit=top_k
    )
    return results.points
