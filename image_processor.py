from image_desc import extract_image
from image_exif import extract_exif
from db_connection import mark_processing_metadata as mark_processing
from db_connection import mark_processed_metadata as mark_processed
from db_connection import get_new_images
from db_connection import upsert_image_metadata
import time
from log import logger
def process_batch():
    files = get_new_images(limit=10)

    for f in files:
        mark_processing(f["file_id"])

    for f in files:
        logger.info("Image is being processed:",f["file_path"])
        desc = extract_image(f["file_path"])
        exif = extract_exif(f["file_path"])

        upsert_image_metadata(f["file_id"],f["file_path"], desc, exif)
        mark_processed(f["file_id"])
        print("Processed:",f["file_id"])



if __name__ == "__main__":
    while True:
        process_batch()
        time.sleep(2)
