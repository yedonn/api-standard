from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
import subprocess
import time

class ChangeHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith('.py'):
            print(f"Detected change in {event.src_path}. Generating migration...")
            subprocess.run(['python', 'generate_migrations.py'])

if __name__ == "__main__":
    path = 'app/db/models'
    event_handler = ChangeHandler()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    
    observer.join()
