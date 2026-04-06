from db.image_repo import mark_processed_metadata
from db.image_repo import mark_processing_metadata
from db.image_repo import upsert_image_metadata
from db.file_repo import mark_processed
from tasks.extraction.extract_image import extract_image
from tasks.extraction.extract_exif import extract_exif
from core.log import logger


def process_image(file):
    # DB state handled here
    logger.info(f"[SERVICE] Processing {file['file_id']} image")

    mark_processing_metadata(file["file_id"])
    desc = extract_image(file["file_path"])
    exif = extract_exif(file["file_path"])
    upsert_image_metadata(file["file_id"], file["file_path"], desc, exif)
    mark_processed_metadata(file["file_id"])
    mark_processed(file["file_path"])
