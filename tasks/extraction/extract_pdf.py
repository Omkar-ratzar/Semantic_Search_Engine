#for pdfs
import fitz  # PyMuPDF
from core.log import logger
from core.errors import safe_execution
from db.file_repo import mark_processed
from core.utils import normalize_path

@safe_execution(component="EXTRACTOR",log_args=True)
def extract_pdf(path):
    doc = fitz.open(path)
    text = ""
    for page in doc:
        text += page.get_text()
    mark_processed(normalize_path(path))
    logger.info("PDF has been extracted. Path:"+path)
    return text
