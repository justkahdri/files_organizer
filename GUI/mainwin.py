import sys
import webbrowser

from mainwin_ui import *
from settings import load_preferences


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        # Connections & Events
        self.startButton.clicked.connect(self.start_observer)
        self.stopButton.clicked.connect(self.stop_observer)
        self.checkGroup.stateChanged.connect(self.group_ungroup)
        self.restoreButton.clicked.connect(lambda: self.display_info(True))
        self.saveButton.clicked.connect(self.save_changes)
        self.actionOpen_route_folder.triggered.connect(lambda: self.open_browser(self.pathroute.text()))
        self.actionReport_bug.triggered.connect(
            lambda: self.open_browser(r"https://github.com/justkahdri/files_organizer/issues/new"))

        # Initialize from json
        self.display_info()

        # Placeholders
        self.consoleLog.setText('The last modifications will appear here')

    def start_observer(self):
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.settingsBox.setEnabled(False)
        self.programStatus.setText('The program is running!')
        self.programStatus.setStyleSheet("QLabel { color : green; }")
        # TODO Sent signal to managers.py

    def stop_observer(self):
        self.stopButton.setEnabled(False)
        self.startButton.setEnabled(True)
        self.settingsBox.setEnabled(True)
        self.programStatus.setText('The program is off.')
        self.programStatus.setStyleSheet("QLabel {}")
        # TODO Sent signal to managers.py

    def group_ungroup(self, checked):
        self.foldername_group.setEnabled(checked)

    def save_changes(self):
        self.consoleLog.setText('New preferences saved!')
        self.consoleLog.setStyleSheet("QLabel { color : green; }")
        # TODO Save to json & check if there are any changes

    def display_info(self, restore=False):
        info = load_preferences()
        self.pathroute.setText(info['search-path'])
        self.foldername_group.setText(info['group-files']['folder'])
        for i in self.settingsBox.children():
            if isinstance(i, QtWidgets.QCheckBox):
                if i.text() in info['extensions'] or (i is self.checkGroup and info['group-files']['active']):
                    i.setChecked(True)
        if restore:
            self.consoleLog.setText('Preferences restored succesfully.')
            self.consoleLog.setStyleSheet("QLabel { color : darkblue; }")

    def open_browser(self, path: str):
        webbrowser.open(path, new=2)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
