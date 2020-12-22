# TODO
# Renombrar los archivos
# Detectar que termino la descarga
# Ignorar archivos temporales y de peso 0kb
import os
import time
from watchdog.observers import Observer
from watchdog.events import FileSystemEvent


def dispatch(event):
    if event.event_type == 'created':
        new_file = str(event.src_path).split('\\')[-1]
        print(f"hey, {new_file} has been created!")
        # os.rename(f'{event.src_path}', f'{path}/newFiles/{new_file}')
    if event.event_type == 'modified':
        print(f"hey buddy, {event.src_path} has been modified")


if __name__ == "__main__":
    path = 'C:/Users/Joaquin/Downloads'
    my_event_handler = FileSystemEvent(path)

    my_event_handler.dispatch = dispatch

    go_recursively = True
    my_observer = Observer()
    my_observer.schedule(my_event_handler, path, recursive=go_recursively)

    my_observer.start()
    try:
        while True:
            time.sleep(2)
    except KeyboardInterrupt:
        my_observer.stop()
        my_observer.join()
