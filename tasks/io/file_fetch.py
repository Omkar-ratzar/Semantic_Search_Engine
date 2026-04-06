# tasks/io/file_fetch.py

from db.image_repo import get_new_images
from db.file_repo import get_file_id_by_path
from config.config import config

limit= config["batch"]["image_processing_batch_size"]

def fetch_new_images(limit: int = limit):
    """
    Returns list of dicts:
    [{ "file_id": int, "file_path": str }, ...]
    """
    return get_new_images(limit)


def fetch_file_id(path: str):
    """
    Resolve file_id from file_path
    """
    return get_file_id_by_path(path)
