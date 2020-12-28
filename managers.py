import os
import time
from threading import Thread
TEMP_EXT = ('bc', 'bc!', 'blf', 'cache', 'crdownload', 'download', 'part', 'partial', 'tmp', 'temp')
IMAGES = ('png', 'jpg', 'gif', 'jpeg')
PATH = 'C:/Users/Joaquin/Downloads/'


class FileManager(Thread):
    def __init__(self, unknowns=False):
        Thread.__init__(self)
        self.stop = False
        self.unknowns = unknowns                # Made to recognise unknown file types (or not)

    def run(self):
        while not self.stop:                    # Loop this infinitely until I tell it stop
            files = os.listdir(PATH)

            for f in files:
                extension = f.split('.')[-1]
                if extension not in TEMP_EXT:  # Checks if the file's last extension is temporary
                    file_type = 'Unknown file'
                    if extension in IMAGES:
                        os.rename(PATH + f, f'C:/Users/Joaquin/Pictures/{f}')
                        file_type = 'Image'
                    if self.unknowns or file_type != 'Unknown file':
                        print(f"{file_type} found", end=' ')
                else:
                    print(f'{f} is a temporary file', end=' ')

            time.sleep(5)
            print("\rProgram running [S̲top]", end='')
        print('\r' + "-"*50)