# TODO
# Ask user if wants to change the observed folder (Downloads by default)
# Save used directories in path.csv
# Ask user what file types wants to filter (All by default)
# Ask user if wants to save the files in a separated folder
# If thats the case, ask for folders name (automanaged by default)
import json


def _change_preferences(new_value, field='search_path'):
    # Opening JSON file
    with open('data/preferences.json', 'r+') as f:
        data = json.load(f)
        data[field] = new_value  # <--- modify `field` value.
        f.seek(0)  # <--- should reset file position to the beginning.
        json.dump(data, f, indent=4)
        f.truncate()  # remove remaining part

    print('Updated', field)
