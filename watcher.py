from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os
from db_connection import upsert_file, mark_modified, mark_deleted, move_file, mark_renamed,get_file_id_by_path,upsert_image_metadata,mark_invalid
from log import logger
from config import config
from error_decorator import safe_execution
from Validator import is_valid



watcher_path=config["paths"]["watcher"]

def wait_for_file_ready(path, retries=5, delay=0.5):
    last_size = -1
    for _ in range(retries):
        if not os.path.exists(path):
            return False
        size = os.path.getsize(path)
        if size == last_size:
            return True
        last_size = size
        time.sleep(delay)
    return False
def normalize_path(path):
    return os.path.abspath(path)

class MyHandler(FileSystemEventHandler):
    def __init__(self):
        self._last_seen = {}

    def should_process(self, path, threshold=1):
        now = time.time()
        if path in self._last_seen and now - self._last_seen[path] < threshold:
            return False
        self._last_seen[path] = now
        return True

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
        if not self.should_process(path):
            return
        logger.info("File added: "+path)
        path = normalize_path(path)
        print("File added: "+path)
        if not wait_for_file_ready(path):
            logger.warning(f"File not ready: {path}")
            return
        upsert_file(path) #need to upsert file first so aa row will be created to mark as invalid
        if(is_valid(path)):
            if path.lower().endswith((".jpg", ".jpeg", ".png")):
                file_id = get_file_id_by_path(path)
                upsert_image_metadata(file_id, path, None, None, status="NEW")
        else:
            mark_invalid(path)


    @safe_execution(component="WATCHER",log_args=True)
    def handle_modified(self, path):
        if not self.should_process(path):
            return
        if not os.path.exists(path):
            return
        path = normalize_path(path)
        logger.info("File modified: "+path)
        print("File modified: "+path)
        if(is_valid(path)):
            mark_modified(path)
            if path.lower().endswith((".jpg", ".jpeg", ".png")):
                file_id = get_file_id_by_path(path)
                upsert_image_metadata(file_id, path, None, None, status="NEW")
        else:
            mark_invalid(path)


    @safe_execution(component="WATCHER",log_args=True)
    def handle_deleted(self, path):
        if not self.should_process(path):
            return
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
        if not self.should_process(src_path):
            return
        src_path = normalize_path(src_path)
        dest_path = normalize_path(dest_path)
        if os.path.dirname(src_path) == os.path.dirname(dest_path):
            if(is_valid(dest_path)):
                mark_renamed(src_path,dest_path)
                logger.info("File renamed: "+dest_path)
                print("File renamed: "+dest_path)
            else:
                mark_invalid(dest_path)
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
