# TODO
# Save used directories in path.csv
# Ask user if wants to save the files in a separated folder
# If thats the case, ask for folders name (automanaged by default)
import json
import os
from shutil import copyfile


def save_paths(value):
    cloned = False
    if os.path.exists("data/u-paths.dat"):
        f = open('data/u-paths.dat', 'r')
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
        data['group_files']['active'] = not data['group_files']['active']
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    print("The file's groups are now " + ('enabled' if data['group_files']['active'] else 'disabled'))


def filter_extensions(new_values: list):
    with open('data/u-preferences.json', 'r+') as f:
        data = json.load(f)
        data['extensions'] = new_values
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()

    print('Extensions updated')


def load_preferences():
    with open('data/u-preferences.json', 'r') as f:
        data = json.load(f)
        return data


def to_default_values(warn=True):
    copyfile('data/default_config.json', 'data/u-preferences.json')
    change_focus('Downloads', warn=False)
    if warn:
        print('Preferences set to default')
