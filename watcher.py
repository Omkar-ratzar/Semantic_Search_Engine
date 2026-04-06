from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
from db_connection import upsert_file, mark_modified, mark_deleted, move_file, mark_renamed,get_file_id_by_path,upsert_image_metadata
from log import logger
from config import config
from error_decorator import safe_execution

watcher_path=config["paths"]["watcher"]

def normalize_path(path):
    return os.path.abspath(path)

class MyHandler(FileSystemEventHandler):

    def on_created(self, event):
        if not event.is_directory:
            self.handle_created(event.src_path)

    def on_modified(self, event):
        if not event.is_directory:
            self.handle_modified(event.src_path)

    def on_deleted(self, event):
        if not event.is_directory:
            self.handle_deleted(event.src_path)

    def on_moved(self, event):
        if not event.is_directory:
            self.handle_moved(event.src_path, event.dest_path)

    # ---- Your logic goes here ----
    @safe_execution(component="WATCHER",log_args=True)
    def handle_created(self, path):
        logger.info("File added: "+path)
        path = normalize_path(path)
        print("File added: "+path)
        upsert_file(path)
        if path.lower().endswith((".jpg", ".jpeg", ".png")):
            file_id = get_file_id_by_path(path)
            upsert_image_metadata(file_id, path, None, None, status="NEW")


    @safe_execution(component="WATCHER",log_args=True)
    def handle_modified(self, path):
        path = normalize_path(path)
        logger.info("File modified: "+path)
        print("File modified: "+path)
        mark_modified(path)
        if path.lower().endswith((".jpg", ".jpeg", ".png")):
            file_id = get_file_id_by_path(path)
            upsert_image_metadata(file_id, path, None, None, status="NEW")


    @safe_execution(component="WATCHER",log_args=True)
    def handle_deleted(self, path):
        path = normalize_path(path)
        logger.info("File deleted: "+path)
        print("File deleted: "+path)
        mark_deleted(path)
        if path.lower().endswith((".jpg", ".jpeg", ".png")):
            file_id = get_file_id_by_path(path)
            if(file_id):
                upsert_image_metadata(file_id, path, None, None, status="DELETED")

    @safe_execution(component="WATCHER",log_args=True)
    def handle_moved(self, src_path, dest_path):
        src_path = normalize_path(src_path)
        dest_path = normalize_path(dest_path)
        if os.path.dirname(src_path) == os.path.dirname(dest_path):
            mark_renamed(src_path,dest_path)
            logger.info("File renamed: "+dest_path)
            print("File renamed: "+dest_path)
        else:
            move_file(src_path, dest_path)
            logger.info("File moved elsewhere: "+dest_path)
            print("File moved elsewhere: "+dest_path)


@safe_execution(component="WATCHER",log_args=True)
def start_watcher(path="."):
    event_handler = MyHandler()
    observer = Observer()
    observer.schedule(event_handler, path=path, recursive=False)
    observer.start()
    print(f"[+] Watching directory: {path}")
    logger.info("Started watcher in:"+(path))
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()

    observer.join()

if __name__ == "__main__":
    start_watcher(watcher_path)
