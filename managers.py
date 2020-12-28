import os
import time
from threading import Thread
TEMP_EXT = ('bc', 'bc!', 'blf', 'cache', 'crdownload', 'download', 'part', 'partial', 'tmp', 'temp')
EXTENSIONS = {
    'Pictures': ('png', 'jpg', 'gif', 'jpeg', 'ai', 'bmp', 'ico', 'ps', 'psd', 'svg', 'tif', 'tiff', 'webp'),
    'Videos': ('.3g2', '3gp', 'avi', 'flv', 'h264', 'm4v', 'mkv', 'mov','mp4', 'mpg', 'mpeg', 'rm', 'swf', 'vob', 'wmv'),
    'Music': ('aif', 'cda', 'mid', 'midi', 'mp3', 'mpa', 'ogg', 'wav', 'wma', 'wpl'),
    'Documents': ('doc', 'docx', 'pdf', 'odt', 'wpd', 'rtf', 'tex')
              }
USER_PATH = os.environ['USERPROFILE']
PATH = USER_PATH + '\\Downloads'


def make_counter():
    counter = {}
    for k in EXTENSIONS.keys():
        counter[k] = 0
    return counter


def print_files_found(counter):
    not_zero = [k for k in counter.keys() if counter[k] != 0]

    if not_zero:
        print(f"\r{counter[not_zero[0]]} {not_zero[0]} file(s) found", end='')
        if len(not_zero) > 1:
            for i in not_zero[1:-1]:
                print(f" - {counter[i]} {i} file(s) found", end='')
            print(f" - {counter[not_zero[-1]]} {not_zero[-1]} file(s) found")
        else:
            print()


def save_file(f, t, i = 0):
    try:
        if i == 0:
            os.rename(f'{PATH}/{f}', f'{USER_PATH}/{t}/automanaged/{f}')
        else:
            os.rename(f'{PATH}/{f}', f'{USER_PATH}/{t}/automanaged/{i}-{f}')
    except FileExistsError:
        save_file(f, t, i+1)
    except FileNotFoundError:
        os.mkdir(f'{USER_PATH}/{t}/automanaged')
        save_file(f, t)


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

            print_files_found(counter)
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
