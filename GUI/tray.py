from PyQt5 import QtWidgets, QtGui


class SystemTrayIcon(QtWidgets.QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QtWidgets.QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip('File Organizer 2.0')
        menu = QtWidgets.QMenu(parent)
        self.parent = parent

        open_folder = menu.addAction('Open route folder')
        # FIXME open_folder.triggered.connect(lambda: self.parent.open_browser(self.parent.pathroute.text()))
        open_folder.setIcon(QtGui.QIcon("icons/blue-folder-smiley.png"))

        resume = menu.addAction("Start")
        resume.triggered.connect(lambda: self.parent.start_observer(False))
        resume.setIcon(QtGui.QIcon("icons/control.png"))

        pause = menu.addAction("Stop")
        pause.triggered.connect(lambda: self.parent.stop_observer(False))
        pause.setIcon(QtGui.QIcon("icons/control-stop-square.png"))

        menu.addSeparator()
        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIconActivated)

        open_app = menu.addAction("Open App")
        open_app.triggered.connect(self.parent.show)
        # TODO close

        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(lambda: sys.exit())
        exit_.setIcon(QtGui.QIcon("icons/control-power.png"))

    def start(self):
        self.show()
        self.showMessage('Files Organizer 2', 'Running in the background')

    def onTrayIconActivated(self, reason):
        if reason == self.DoubleClick:
            self.parent.show()
            self.hide()


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = QtWidgets.QMainWindow()
    app.setQuitOnLastWindowClosed(False)
    tray_icon = SystemTrayIcon(QtGui.QIcon("icons/Logo.png"), window)
    tray_icon.start()
    sys.exit(app.exec_())
