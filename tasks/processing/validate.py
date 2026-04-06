from config.config import config
import os
import magic

BASE_DIR = config["paths"]["watcher"]

# =========================
# QUERY VALIDATION
# =========================
def is_valid_query(q: str) -> bool:
    return bool(q)

def is_valid(path):
    return bool(validate_path(path)) and bool(is_valid_extension(path))
# =========================
# IMAGE OUTPUT VALIDATION
# =========================
def is_valid_image_output(text: str) -> bool:
    required_sections = [
        "[SCENE TYPE]:",
        "[PRIMARY SUBJECTS]:",
    ]
    return any(sec in text for sec in required_sections)


# =========================
# FILE VALIDATION
# =========================
import os
import magic

EXTENSION_TO_MIME = {
    ".pdf": {"application/pdf"},
    ".docx": {"application/vnd.openxmlformats-officedocument.wordprocessingml.document"},
    ".pptx": {"application/vnd.openxmlformats-officedocument.presentationml.presentation"},
    ".jpg": {"image/jpeg", "image/pjpeg"},
    ".jpeg": {"image/jpeg", "image/pjpeg"},
    ".png": {"image/png"},
    ".doc": {"application/msword", "application/octet-stream", "application/x-ole-storage"}
}


def validate_path(path: str, base_dir: str = BASE_DIR) -> bool:
    if not os.path.exists(path):
        return False

    if os.path.islink(path):
        return False

    real_path = os.path.realpath(path)
    base_dir = os.path.realpath(base_dir)

    return real_path.startswith(base_dir + os.sep)


def is_valid_extension(path: str) -> bool:
    if not os.path.isfile(path):
        return False

    ext = os.path.splitext(path)[1].lower()
    if not ext:
        return False

    expected_mimes = EXTENSION_TO_MIME.get(ext)
    if not expected_mimes:
        return False

    try:
        actual_mime = magic.from_file(path, mime=True)
    except:
        return False

    return actual_mime in expected_mimes


def is_valid_file(path: str, base_dir: str) -> bool:
    return validate_path(path, base_dir) and is_valid_extension(path)
