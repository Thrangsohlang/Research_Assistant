from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import time
import os

INCOMING_DIR = "./incoming_journals"
PROCESSED_LOG = "./processed_files.txt"

class JournalHandler(FileSystemEventHandler):
    def __init__(self):
        self.processed = self._load_processed()

    def _load_processed(self):
        if not os.path.exists(PROCESSED_LOG):
            return set()
        with open(PROCESSED_LOG) as f:
            return set(line.strip() for line in f)

    def _mark_processed(self, filename):
        self.processed.add(filename)
        with open(PROCESSED_LOG, "a") as f:
            f.write(filename + "\n")

    def on_created(self, event):
        # only handle files, not directories
        if event.is_directory:
            return

        filename = os.path.basename(event.src_path)
        if not filename.lower().endswith((".pdf", ".docx", ".json")):  # NOTE: Can add more file ext here
            return

        if filename in self.processed:
            return  # already handled

        # Mark before processing to avoid races
        self._mark_processed(filename)
        print(f"New journal detected: {filename}")
        
        # TODO: call your chunking_pipeline(event.src_path)

if __name__ == "__main__":
    handler = JournalHandler()
    observer = Observer()
    observer.schedule(handler, path=INCOMING_DIR, recursive=False)
    observer.start()
    print(f"Watching for new journals in {INCOMING_DIR}…")
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()
