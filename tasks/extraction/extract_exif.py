from PIL import Image
from PIL.ExifTags import TAGS

def extract_exif(path):
    try:
        img = Image.open(path)
        exif_data = {}
        if img._getexif():
            for tag, val in img._getexif().items():
                key = TAGS.get(tag, tag)
                exif_data[key] = str(val)
        return exif_data
    except Exception as e:
        return {"error": str(e)}

