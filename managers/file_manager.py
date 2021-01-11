import os
import time
from threading import Thread
USER_PATH = os.environ['USERPROFILE']


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


def load_extensions():
    with open('../data/extensions.dat') as f:
        to_dict = eval(f.read())
        return to_dict.items()


class FileManager(Thread):
    def __init__(self, pref: dict, unknowns=False):
        Thread.__init__(self)
        self.stop = False
        self.path = pref['search-path']
        self.filetypes = {k: e for k, e in load_extensions() if k in pref['extensions']}
        self.group_folder = pref['group-files']['folder'] if pref['group-files']['active'] else None
        self.unknowns = unknowns                        # Made to recognise unknown file types (or not)

    def run(self):
        while not self.stop:                            # Loop this infinitely until I tell it stop
            files = os.listdir(self.path)

            counter = self.make_counter()

            print("\rProgram running [S̲top]", end='')

            for f in files:
                if os.path.getsize(f'{self.path}/{f}'):
                    file_type = self.find_extension(f)
                    if self.unknowns or file_type != 'Unknown':
                        counter[file_type] += 1

            print_files_found(counter)
            time.sleep(5)

        print('\r' + "-"*50)

    def make_counter(self):
        counter = {'Unknown': 0}
        for k in self.filetypes.keys():
            counter[k] = 0
        return counter

    def find_extension(self, filename):
        current_ext = filename.split('.')[-1]
        for file_type, ext in self.filetypes.items():
            if current_ext in ext and file_type != 'Temporal':
                self.save_file(filename, file_type)
                return file_type
        return 'Unknown'

    def save_file(self, f, subfolder, i=0):
        if self.group_folder and i == 0:
            subfolder += f'/{self.group_folder}'
        try:
            if i == 0:
                os.rename(f'{self.path}/{f}', f'{USER_PATH}/{subfolder}/{f}')
            else:
                os.rename(f'{self.path}/{f}', f'{USER_PATH}/{subfolder}/{i}-{f}')
        except FileExistsError:
            self.save_file(f, subfolder, ++i)
        except FileNotFoundError:
            os.mkdir(f'{USER_PATH}/{subfolder}')
            self.save_file(f, subfolder)
