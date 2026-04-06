import sys

from pipelines.image_pipeline import run as run_images
from pipelines.document_pipeline import run as run_docs

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "all"

    if mode == "image":
        run_images()
    elif mode == "doc":
        run_docs()
    elif mode == "all":
        run_images()
        run_docs()
