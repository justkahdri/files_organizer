from webbrowser import open as navigate
import os.path

from GUI.mainwin_ui import *
from GUI.tray import SystemTrayIcon
from GUI.restore_alert import RestoreAlert

from managers.file_manager import FileManager
import managers.settings as stg


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.robot = None
        self.tray_icon = SystemTrayIcon(QtGui.QIcon("icons/Logo.png"), self)

        # Connections & Events
        self.startButton.clicked.connect(lambda: self.start_observer())
        self.stopButton.clicked.connect(lambda: self.stop_observer())
        self.checkGroup.stateChanged.connect(lambda x: self.foldername_group.setEnabled(x))
        self.restoreButton.clicked.connect(lambda: self.display_info())
        self.saveButton.clicked.connect(self.save_changes)
        self.browser_searchPath.clicked.connect(self.pass_path)

        # MenuBar Actions
        self.actionRestore_settings.triggered.connect(lambda: restore_alert.show())
        self.actionOpen_route_folder.triggered.connect(lambda: self.open_browser(self.pathroute.text()))
        self.actionReport_bug.triggered.connect(
            lambda: self.open_browser(r"https://github.com/justkahdri/files_organizer/issues/new"))

        # Initialize from json
        self.display_info()

        # Placeholders
        self.console_placeholder.close()

    def start_observer(self, main_window=True):
        if self.compare_saved_settings():
            self.print_console('You have changes without saving!', 'QLabel { color : darkred; }')
            return False
        if main_window:
            self.startButton.setEnabled(False)
            self.stopButton.setEnabled(True)
            self.settingsBox.setEnabled(False)
            self.programStatus.setText('The program is running!')
            self.programStatus.setStyleSheet("QLabel { color : green; }")
            self.print_console('⬇ The last modifications will appear here ⬇')

        self.robot = FileManager(stg.load_preferences(), self, lambda x: self.print_console(x, 'QLabel { color : darkred; }'))
        self.robot.start()

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
            self.stopButton.setEnabled(False)
            self.settingsBox.setEnabled(True)
            self.programStatus.setText('The program is off.')
            self.programStatus.setStyleSheet("QLabel {}")

    def compare_saved_settings(self):
        extensions = [i for i in self.settingsBox.children()
                      if isinstance(i, QtWidgets.QCheckBox) and i is not self.checkGroup]
        active_extensions = [e.text() for e in extensions if e.isChecked()]
        current_values = {
            'search-path': self.pathroute.text(),
            'group-files': {
                'active': self.checkGroup.isChecked(),
                'folder': self.foldername_group.text()
            },
            'extensions': active_extensions,
            'default-folders': True
        }
        if current_values == stg.load_preferences():
            return False
        else:
            return current_values

    def save_changes(self):
        if not os.path.isdir(self.pathroute.text()):
            self.print_console('Path does not exists')
            # TODO add foldername check
            return False
        changes = self.compare_saved_settings()
        if changes:
            stg.save_to_json(changes)
            self.print_console('New preferences saved!', "QLabel { color : green; }")
        else:
            self.print_console('Make some changes before saving into settings.', "QLabel { color : orange; }")

    def display_info(self):
        changes = self.compare_saved_settings()
        if not changes:
            self.print_console('Preferences not changed.', "QLabel { color : orange; }")
        else:
            info = stg.load_preferences()
            self.pathroute.setText(info['search-path'])
            self.foldername_group.setText(info['group-files']['folder'])
            for i in self.settingsBox.children():
                if isinstance(i, QtWidgets.QCheckBox):
                    if i.text() in info['extensions'] or (i is self.checkGroup and info['group-files']['active']):
                        i.setChecked(True)

    def pass_path(self):
        folder = str(QtWidgets.QFileDialog.getExistingDirectory(self, "Select Directory"))
        self.pathroute.setText(str(folder))

    def print_console(self, text: str, style=None):
        label = QtWidgets.QLabel()
        label.setText(text)
        if style:
            label.setStyleSheet(style)
        self.verticalLayout.addStretch()
        self.verticalLayout.insertWidget(self.verticalLayout.count() - 1, label)
        # FIXME self.consoleScroll.ensureVisible(0, self.consoleScroll.height(), 0, 0)

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
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    restore_alert = RestoreAlert(parent=window)
    window.show()
    app.exec_()
