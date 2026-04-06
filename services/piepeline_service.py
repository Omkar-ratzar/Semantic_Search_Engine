from .image_service import process_image
from db.image_repo import get_new_images

from .document_service import process_document
from db.file_repo import get_new_documents

def process_new_images(limit):
    files = get_new_images(limit)
    for f in files:
        process_image(f)


def process_documents(limit):
    files = get_new_documents(limit)
    for f in files:
        process_document(f)
