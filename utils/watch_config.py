# watch_config.py
import time
import os
import threading
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class ConfigFileHandler(FileSystemEventHandler):
    def __init__(self, config_path, reload_func):
        self.config_path = config_path
        self.reload_func = reload_func
        self.last_modified_time = os.path.getmtime(self.config_path)

    def on_modified(self, event):
        if not event.is_directory and os.path.normpath(self.config_path) == os.path.normpath(event.src_path):
            current_time = time.time()
            time_interval = current_time - self.last_modified_time
            self.last_modified_time = current_time
            # VSCode编辑文本时会连续保存多次
            if time_interval < 0.5:
                return
            else:
                self.reload_func()
                print(f'配置文件{self.config_path}被修改，重新加载')

def watch_config(config_path, reload_func):
    def watch_config_thread(config_path, reload_func):
        event_handler = ConfigFileHandler(config_path, reload_func)
        observer = Observer()
        observer.schedule(event_handler, '.', recursive=True)
        observer.start()
        try:
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            observer.stop()
        observer.join()
    t = threading.Thread(target=watch_config_thread, args=(config_path, reload_func,))
    t.start()
    return t
