import os
import sys
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from managers import FileManager

class SystemTrayIcon(QSystemTrayIcon):

    def __init__(self, icon, parent=None):
        QSystemTrayIcon.__init__(self, icon, parent)
        self.setToolTip('Tremendo organizador de Archivos')
        menu = QMenu(parent)

        open_app = menu.addAction("Open Notepad")
        open_app.triggered.connect(self.open_notepad)
        open_app.setIcon(QIcon('icons/notepad.png'))

        open_cal = menu.addAction("Open Calculator")
        open_cal.triggered.connect(self.open_calc)
        open_cal.setIcon(QIcon("icons/calc.png"))

        pause = menu.addAction("Pause")
        pause.triggered.connect(self.pause)
        pause.setIcon(QIcon("icons/pause.png"))

        resume = menu.addAction("Resume")
        resume.triggered.connect(self.resume)
        resume.setIcon(QIcon("icons/play.png"))

        menu.addSeparator()
        self.setContextMenu(menu)
        self.activated.connect(self.onTrayIconActivated)

        exit_ = menu.addAction("Exit")
        exit_.triggered.connect(lambda: sys.exit())
        exit_.setIcon(QIcon("icons/power-off.png"))

    def onTrayIconActivated(self, reason):
        # if reason == self.DoubleClick:
        #     self.open_notepad()
        if reason == self.Trigger:
            open_gui()

    def open_notepad(self):
        os.system('notepad')

    def open_calc(self):
        os.system('calc')

    def pause(self):
        robot.stop = True

    def resume(self):
        robot.stop = False
        robot.start()

def open_gui():
    window.show()

def start_tray():
    app.setQuitOnLastWindowClosed(False)
    w = QWidget()
    open_gui()
    icon = QIcon("icons/Logo.png")
    tray_icon = SystemTrayIcon(icon, w)
    tray_icon.show()
    tray_icon.showMessage('AutoManager', 'Ordenando')
    sys.exit(app.exec_())

app = QApplication(sys.argv)
window = QMainWindow()
robot = FileManager()
if __name__ == '__main__':
    start_tray()

