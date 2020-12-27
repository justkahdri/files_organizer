# TODO
# Renombrar los archivos
# Detectar que termino la descarga
# Ignorar archivos temporales y de peso 0kb
import os
import time
TEMP_EXT = ('bc', 'bc!', 'blf', 'cache', 'crdownload', 'download', 'part', 'partial', 'tmp', 'temp')
IMAGES = ('png', 'jpg', 'gif', 'jpeg')
PATH = 'C:/Users/Joaquin/Downloads/'


def files_found(files, unknowns=False):
    for f in files:
        extension = f.split('.')[-1]
        if extension not in TEMP_EXT:                # Checks if the file's last extension is temporary
            file_type = 'Unknown file'
            if extension in IMAGES:
                os.rename(PATH + f, f'C:/Users/Joaquin/Pictures/{f}')
                file_type = 'Image'
            if unknowns or file_type != 'Unknown file':
                print(f"{file_type} found", end=' - ')
        else:
            print(f'El archivo {f} es temporal')


def _print_welcome():
    print('Welcome to the Files Organizer')
    print(f'Currently checking in {PATH}')
    print('⬇ The last modifications will appear here ⬇')


if __name__ == "__main__":
    _print_welcome()
    while True:
        files_found(os.listdir(PATH))
        time.sleep(5)
        print("\r-----", end='')
