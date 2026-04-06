import os
import json
import time

def normalize_path(path: str) -> str:
    return os.path.abspath(path)

def resolve_path(path: str) -> str:
    return os.path.realpath(path)

def is_subpath(path: str, base_dir: str) -> bool:
    path = resolve_path(path)
    base = resolve_path(base_dir)
    return path.startswith(base + os.sep)

def wait_for_file_ready(path, retries=5, delay=0.5):
    last_size = -1
    for _ in range(retries):
        if not os.path.exists(path):
            return False
        size = os.path.getsize(path)
        if size == last_size:
            return True
        last_size = size
        time.sleep(delay)
    return False

def batch_iterable(iterable, batch_size):
    batch = []
    for item in iterable:
        batch.append(item)
        if len(batch) == batch_size:
            yield batch
            batch = []
    if batch:
        yield batch

def normalize_text(text: str) -> str:
    if not text:
        return ""
    return " ".join(text.strip().split())

def safe_json_dumps(data):
    try:
        return json.dumps(data)
    except Exception:
        return None

def safe_json_loads(data):
    try:
        return json.loads(data)
    except Exception:
        return None

def make_chunk_id(file_id: int, chunk_id: int) -> str:
    return f"{file_id}_{chunk_id}"
