from managers import FileManager
from settings import *
from tray import *

def _print_welcome():
    print('Welcome to the Files Organizer\n'
          'What would you like to do today?')
    _print_commands()


def _print_commands():
    print(f'Currently checking in {path}\n'
          '[C]hange observed folder\n'
          '[S]elect filetypes to filter\n'
          '[G]roup or Ungruop files\n'
          '[L]og status\n'
          '[R]eset preferences\n'
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
                chosen = input('What filetypes would you want to look for? (Repeat from above): ').title()
                filter_extensions(chosen.split())
            elif command == 'g':
                group_ungroup()
            elif command == 'l':
                log_status()
            elif command == 'r':
                reset = confirmation('Are you sure you want to set all preferences to default values? Yes/(No) ')
                if reset:
                    to_default_values()
            elif command == 'e':
                break
            elif command == "start":
                print('⬇ The last modifications will appear here ⬇')
                robot = FileManager()
                robot.start()
                start_tray()
            elif command in ['help', 'h']:
                _print_commands()
            else:
                print('Unknown command, try again')

        elif command in ["stop", 's']:
            print('Closing...')
            robot.stop = True
            robot.join()
            robot = None
        else:
            print('Unknown command, try again')
