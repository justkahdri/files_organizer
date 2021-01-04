from managers import FileManager
from settings import *


def _print_welcome():
    print('Welcome to the Files Organizer\n'
          f'Currently checking in {path}\n'
          'What would you like to do today?\n'
          '[C]hange observed folder\n'
          '[S]elect filetypes to filter\n'
          '[G]roup or Ungruop files\n'
          '[L]og status\n'
          '[Start] Observer\n'
          '[H]elp --> Prints this message\n'
          '[E]xit program')


if __name__ == "__main__":
    if not os.path.exists("data/u-preferences.json"):
        to_default_values(warn=False)       # Creates u-preferences.json from default_config.json
    path = load_preferences()['search-path']
    robot = None
    _print_welcome()

    while True:
        command = input()
        command.lower()

        if robot is None:
            if command == 'c':
                folder = input('Where do you want me to check?: ')
                change_focus(folder)
            elif command == 's':
                current = load_preferences()['extensions']
                print(f'The current extensions are: {current}')
                chosen = input('What extensions would you want to look for? (Repeat from above): ').title()
                filter_extensions(chosen.split())
            elif command == 'g':
                group_ungroup()
            elif command == 'l':
                print(load_preferences())
            elif command == 'e':
                break
            elif command == "start":
                print('⬇ The last modifications will appear here ⬇')
                robot = FileManager()
                robot.start()
            elif command in ['help', 'h']:
                _print_welcome()
            else:
                print('Unknown command, try again')

        elif command in ["stop", 's']:
            print('Closing...')
            robot.stop = True
            robot.join()
            robot = None
        else:
            print('Unknown command, try again')
