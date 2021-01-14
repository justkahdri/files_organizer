from PyQt5 import QtWidgets, QtGui
from sys import exit


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip('File Organizer 2.0')
        self.menu = QtWidgets.QMenu(parent)
        self.setContextMenu(self.menu)
        self.activated.connect(self.onTrayIconActivated)
        self.parent = parent

        self.open_folder = self.menu.addAction('Open route folder')
        self.open_folder.triggered.connect(lambda: self.parent.open_browser(self.parent.pathroute.text()))
        self.open_folder.setIcon(QtGui.QIcon("icons/blue-folder-smiley.png"))

        self.resume = self.menu.addAction("Start")
        self.resume.triggered.connect(lambda: self.parent.start_observer())
        self.resume.setIcon(QtGui.QIcon("icons/control.png"))

        self.pause = self.menu.addAction("Stop")
        self.pause.setEnabled(False)
        self.pause.triggered.connect(lambda: self.parent.stop_observer())
        self.pause.setIcon(QtGui.QIcon("icons/control-stop-square.png"))

        self.menu.addSeparator()
        self.open_app = self.menu.addAction("Open App")
        self.open_app.triggered.connect(self.close_tray)

        self.exit_ = self.menu.addAction("Exit")
        self.exit_.triggered.connect(lambda: exit())
        self.exit_.setIcon(QtGui.QIcon("icons/control-power.png"))

    def start(self):
        self.show()
        self.showMessage('Files Organizer 2', 'Running in the background')

    def enable_disable(self, start):
        if start:
            self.resume.setEnabled(False)
            self.pause.setEnabled(True)
        else:
            self.resume.setEnabled(True)
            self.pause.setEnabled(False)

    def close_tray(self):
        self.parent.show()
        self.hide()

    def onTrayIconActivated(self, reason):
        if reason == self.DoubleClick:
            self.close_tray()


if __name__ == '__main__':
    from sys import argv

    app = QtWidgets.QApplication(argv)
    window = QtWidgets.QMainWindow()
    app.setQuitOnLastWindowClosed(False)
    tray_icon = SystemTrayIcon(QtGui.QIcon("icons/Logo.png"), window)
    tray_icon.start()
    app.exec_()
