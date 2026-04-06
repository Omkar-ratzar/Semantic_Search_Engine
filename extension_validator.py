import magic
import os
from error_decorator import safe_execution
from log import logger

EXTENSION_TO_MIME = {
    ".pdf": {"application/pdf"},
    ".docx": {"application/vnd.openxmlformats-officedocument.wordprocessingml.document"},
    ".pptx": {"application/vnd.openxmlformats-officedocument.presentationml.presentation"},
    ".jpg": {"image/jpeg", "image/pjpeg"},
    ".jpeg": {"image/jpeg", "image/pjpeg"},
    ".png": {"image/png"},
    ".doc": {"application/msword", "application/octet-stream", "application/x-ole-storage"}
}

@safe_execution(component="EXTENSION_VALIDATOR")
def is_valid_extension(path):
    if not os.path.isfile(path):
        logger.error(f"File does not exist: {path}")
        return False

    ext = os.path.splitext(path)[1].lower()

    if not ext:
        logger.error(f"Missing file extension: {path}")
        return False

    expected_mimes = EXTENSION_TO_MIME.get(ext)
    if not expected_mimes:
        logger.error(f"Unsupported extension: {ext} | {path}")
        return False

    try:
        actual_mime = magic.from_file(path, mime=True)
    except Exception as e:
        logger.error(f"MIME detection failed: {path} | {e}")
        return False

    if actual_mime not in expected_mimes:
        logger.warning(
            f"MIME mismatch: expected {expected_mimes}, got {actual_mime} | {path}"
        )
        return False

    return True

# print(is_valid_extension("./data/computer.docx"))
