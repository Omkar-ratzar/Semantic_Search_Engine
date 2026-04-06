from services.piepeline_service import process_documents
from config.config import config
from core.log import logger
limit= config["batch"]["file_processing_batch_size"]
def run():
    logger.info(f"[PIPELINE] Processing {limit} documents")
    process_documents(limit=limit)
