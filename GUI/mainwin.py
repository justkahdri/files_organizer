import sys
import asyncio

from GUI.mainwin_ui import *
from GUI.tray import SystemTrayIcon
from managers.file_manager import FileManager
from managers.settings import load_preferences
from webbrowser import open as navigate


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.robot = None
        self.tray_icon = SystemTrayIcon(QtGui.QIcon("icons/Logo.png"), self)

        # Connections & Events
        self.startButton.clicked.connect(lambda: self.start_observer())
        self.stopButton.clicked.connect(lambda: self.stop_observer())
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

    def stop_observer(self, main_window=True):
        # if main_window:
        #     self.stopButton.setEnabled(False)
        #     self.programStatus.setText('Closing...')
        #     self.programStatus.setStyleSheet("QLabel { color: red; }")
        self.robot.stop = True
        self.robot.join(0.1)
        self.robot = None
        if main_window:
            self.startButton.setEnabled(True)
            self.settingsBox.setEnabled(True)
            self.programStatus.setText('The program is off.')
            self.programStatus.setStyleSheet("QLabel {}")

    def start_observer(self, main_window=True):
        if main_window:
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(True)
            self.settingsBox.setEnabled(False)
            self.programStatus.setText('The program is running!')
            self.programStatus.setStyleSheet("QLabel { color : green; }")

        self.consoleLog.setText('⬇ The last modifications will appear here ⬇')
        self.consoleLog.setStyleSheet("QLabel {}")
        self.robot = FileManager(load_preferences())
        self.robot.start()

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

    @staticmethod
    def open_browser(path: str):
        navigate(path, new=2)

    def closeEvent(self, event):
        if self.actionMinimize.isChecked():
            event.ignore()
            self.hide()
            self.tray_icon.start()
        else:
            self.tray_icon.close()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
