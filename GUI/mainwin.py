import sys

from mainwin_ui import *
from settings import load_preferences


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):

    def __init__(self, *args, **kwargs):
        QtWidgets.QMainWindow.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.display_info()
        self.consoleLog.setText('The last modifications will appear here')
        self.startButton.clicked.connect(self.start_observer)
        self.stopButton.clicked.connect(self.stop_observer)

    def start_observer(self):
        self.startButton.setEnabled(False)
        self.stopButton.setEnabled(True)
        self.settingsBox.setEnabled(False)
        # Sent signal to managers.py

    def stop_observer(self):
        self.stopButton.setEnabled(False)
        self.startButton.setEnabled(True)
        self.settingsBox.setEnabled(True)
        # Sent signal to managers.py

    def display_info(self):
        info = load_preferences()

        self.pathroute.setText(info['search-path'])
        for i in self.settingsBox.children():
            if isinstance(i, QtWidgets.QCheckBox):
                if i.text() in info['extensions'] or (i is self.title_group and info['group-files']['active']):
                    i.setChecked(True)


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec_()
