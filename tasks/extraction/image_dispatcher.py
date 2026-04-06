from .extract_image import extract_image
from .extract_exif import extract_exif

def process_image(path):
    desc = extract_image(path)
    exif = extract_exif(path)

    return {
        "description": desc,
        "exif": exif
    }
