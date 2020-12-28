import os
import time
from threading import Thread
TEMP_EXT = ('bc', 'bc!', 'blf', 'cache', 'crdownload', 'download', 'part', 'partial', 'tmp', 'temp')
EXTENSIONS = {'Pictures': ('png', 'jpg', 'gif', 'jpeg', 'ai', 'bmp', 'ico', 'ps', 'psd', 'svg', 'tif', 'tiff', 'webp'),
              'Videos': ('.3g2', '3gp', 'avi', 'flv', 'h264', 'm4v', 'mkv', 'mov',
                         'mp4', 'mpg', 'mpeg', 'rm', 'swf', 'vob', 'wmv'),
              'Music': ('aif', 'cda', 'mid', 'midi', 'mp3', 'mpa', 'ogg', 'wav', 'wma', 'wpl')}
USER_PATH = os.environ['USERPROFILE']
PATH = USER_PATH + '/Downloads'


def make_counter():
    counter = {}
    for k in EXTENSIONS.keys():
        counter[k] = 0
    return counter


def is_empty(counter):
    empty = True
    for k, v in counter.items():
        if v > 0:
            print(f"\r{v} {k} file(s) found", end=' ')
            empty = False
    return empty


def save_file(f, t, i = 0):
    try:
        if i != 0:
            os.rename(f'{PATH}/{f}', f'{USER_PATH}/{t}/{i}{f}')
        else:
            os.rename(f'{PATH}/{f}', f'{USER_PATH}/{t}/{f}')
    except FileExistsError:
        save_file(f, t, int(i)+1)


class FileManager(Thread):
    def __init__(self, unknowns=False):
        Thread.__init__(self)
        self.stop = False
        self.unknowns = unknowns                        # Made to recognise unknown file types (or not)

    def run(self):
        while not self.stop:                            # Loop this infinitely until I tell it stop
            files = os.listdir(PATH)

            counter = make_counter()

            print("\rProgram running [S̲top]", end='')

            for f in files:
                current_ext = f.split('.')[-1]
                if current_ext not in TEMP_EXT:         # Checks if the file's last extension is temporary
                    file_type = self.find_extension(f)
                    if self.unknowns or file_type != 'Unknown file':
                        counter[file_type] += 1

            if not is_empty(counter):
                print()

            time.sleep(5)

        print('\r' + "-"*50)

    @staticmethod
    def find_extension(filename):
        current_ext = filename.split('.')[-1]
        for file_type, ext in EXTENSIONS.items():
            if current_ext in ext:
                save_file(filename, file_type)
                return file_type
        return 'Unknown file'
