# TODO
# Save used directories in path.csv
# Ask user if wants to save the files in a separated folder
# If thats the case, ask for folders name (automanaged by default)
import json
import os
import pandas


def save_paths(value):
    try:
        df = pandas.read_csv('data/u-paths.csv')
        df.append([value])
    except pandas.errors.EmptyDataError:
        df = pandas.DataFrame([value])
    df.to_csv('data/paths.csv', index=False, header=False)


def change_focus(folder):
    with open('data/u-preferences.json', 'r+') as f:
        data = json.load(f)
        root = os.environ['USERPROFILE']
        new_route = root + f'\\{folder}'
        save_paths(new_route)

        data['search-path'] = new_route  # <--- modify `field` value.
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()  # remove remaining part

    print(f'Now checking in {new_route}')


def group_ungroup():
    with open('data/u-preferences.json', 'r+') as f:
        data = json.load(f)
        data['group_files']['active'] = not data['group_files']['active']
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()  # remove remaining part

    print("The file's groups are now " + ('enabled' if data['group_files']['active'] else 'disabled'))


def change_preferences(field, new_value):
    # Opening JSON file
    with open('data/u-preferences.json', 'r+') as f:
        data = json.load(f)
        data[field] = new_value  # <--- modify `field` value.
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()  # remove remaining part

    print('Updated', field)


def load_preferences():
    with open('data/u-preferences.json', 'r') as f:
        data = json.load(f)
        return data
