# TODO
# Manage folders
# Recognise more file extensions
# FIXME
# Ignore empty files >> 0kb
from managers import FileManager, PATH


def _print_welcome():
    print('Welcome to the Files Organizer')
    print(f'Currently checking in {PATH}')
    print('⬇ The last modifications will appear here ⬇')


if __name__ == "__main__":
    _print_welcome()
    robot = None

    while True:
        try:
            if robot is None:
                command = input("Enter command [Start]/[S̲top]: ")
                if command == 'e':
                    break
            else:
                command = input()

            if command == "start":
                robot = FileManager()
                robot.start()

            elif command in ["stop", 's']:
                print('Closing...')
                robot.stop = True
                robot.join()
                robot = None
            else:
                print('Unknown command, try again')
        except AttributeError:
            print('There is no program running')
