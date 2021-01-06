import json
import os
from shutil import copyfile


def confirmation(string):
    while True:
        entry = input(string).lower()
        if not entry or entry in ['no', 'n']:
            return False
        elif entry in ['yes', 'y']:
            return True
        else:
            print('Unkown command, please try again')


def save_paths(value):
    cloned = False
    if os.path.exists("data/u-paths.dat"):
        f = open('data/u-paths.dat')
        saved_paths = f.read().splitlines()
        cloned = value in saved_paths
        f.close()

    if not cloned:
        with open('data/u-paths.dat', 'a') as data:
            data.write(value + "\n")


def change_focus(folder, warn=True):
    with open('data/u-preferences.json', 'r+') as f:
        data = json.load(f)
        root = os.environ['USERPROFILE']
        new_route = root + f'\\{folder}'
        save_paths(new_route)

        data['search-path'] = new_route  # <--- modify `field` value.
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()  # remove remaining part

    if warn:
        print(f'Now checking in {new_route}')


def group_ungroup():
    with open('data/u-preferences.json', 'r+') as f:
        data = json.load(f)
        data['group-files']['active'] = not data['group-files']['active']

        if data['group-files']['active']:
            change_folder = confirmation("Do you want to change the folder's name? Yes/(No) ")
            if change_folder:
                new_folder = input('Type the new name: ')
                data['group-files']['folder'] = new_folder

        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    print("The file's groups are now " + ('enabled' if data['group-files']['active'] else 'disabled'))


def filter_extensions(new_values: list):
    with open('data/u-preferences.json', 'r+') as f:
        data = json.load(f)
        data['extensions'] = new_values
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    print('Extensions updated')


def load_preferences():
    with open('data/u-preferences.json') as f:
        data = json.load(f)
        return data


def log_status():
    data = load_preferences()
    print(f"Currently checking {data['search-path']}")
    if data["group-files"]["active"]:
        print(f'Files will be grouped in "{data["group-files"]["folder"]}" folder')
    else:
        print('Grouping files is disabled')
    print(f'Looking for the following filetypes: {", ".join(data["extensions"])}')


def to_default_values(warn=True):
    copyfile('data/default_config.json', 'data/u-preferences.json')
    change_focus('Downloads', warn=False)
    if warn:
        print('Preferences set to default')
