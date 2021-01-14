import json
import os
from shutil import copyfile


def save_paths(value):
    cloned = False
    if os.path.exists("../data/u-paths.dat"):
        f = open('../data/u-paths.dat')
        saved_paths = f.read().splitlines()
        cloned = value in saved_paths
        f.close()

    if not cloned and value:
        with open('../data/u-paths.dat', 'a') as data:
            data.write(value + "\n")


def change_focus(new_route):
    save_paths(new_route)
    with open('../data/u-preferences.json', 'r+') as f:
        data = json.load(f)

        data['search-path'] = new_route
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()  # remove remaining part


def load_preferences():
    try:
        with open('../data/u-preferences.json') as f:
            data = json.load(f)
            return data
    except FileNotFoundError:
        to_default_values()


def enable_disable_tray(boolean):
    with open('../data/u-preferences.json', 'r+') as f:
        data = json.load(f)
        data['system-tray'] = boolean
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


def save_to_json(new_values: dict):
    save_paths(new_values.get('search-path'))
    with open('../data/u-preferences.json', 'r+') as f:
        data = json.load(f)
        final = {k: new_values.get(k) or data.get(k) for k in set(data)}
        f.seek(0)
        json.dump(final, f, indent=4)
        f.truncate()


def to_default_values():
    copyfile('../data/default_config.json', '../data/u-preferences.json')
    change_focus(f'{os.environ["USERPROFILE"]}\\Downloads')
