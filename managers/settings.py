import json
import os
from shutil import copyfile
# TODO check if input values are the same that in the json


def save_paths(value):
    cloned = False
    if os.path.exists("../data/u-paths.dat"):
        f = open('../data/u-paths.dat')
        saved_paths = f.read().splitlines()
        cloned = value in saved_paths
        f.close()

    if not cloned:
        with open('../data/u-paths.dat', 'a') as data:
            data.write(value + "\n")


def change_focus(new_route):
    save_paths(new_route)
    with open('../data/u-preferences.json', 'r+') as f:
        data = json.load(f)

        data['search-path'] = new_route  # <--- modify `field` value.
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()  # remove remaining part


def group_ungroup(active, foldername):
    with open('../data/u-preferences.json', 'r+') as f:
        data = json.load(f)
        if data['group-files']['active'] == active and data['group-files']['folder'] == foldername:
            return True
        data['group-files']['active'] = active
        data['group-files']['folder'] = foldername

        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


def filter_extensions(new_values: list):
    with open('../data/u-preferences.json', 'r+') as f:
        data = json.load(f)
        data['extensions'] = new_values
        f.seek(0)
        json.dump(data, f, indent=4)
        f.truncate()


def load_preferences():
    with open('../data/u-preferences.json') as f:
        data = json.load(f)
        return data


def to_default_values():
    copyfile('../data/default_config.json', '../data/u-preferences.json')
    change_focus(f'{os.environ["USERPROFILE"]}\\Downloads')
