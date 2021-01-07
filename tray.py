import sys
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QSystemTrayIcon, QMenu, QWidget, QMainWindow

app = QApplication(sys.argv)
app.setQuitOnLastWindowClosed(False)

window = QMainWindow()
window.show()

icon = QIcon("data/AutoManager.png")
tray = QSystemTrayIcon()
tray.setIcon(icon)
tray.setToolTip('Tremendo organizador de Archivos')
tray.setVisible(True)

menu = QMenu()
if QSystemTrayIcon.Trigger:
    window.show()

quit = menu.addAction('Exit')
quit.triggered.connect(app.quit)

tray.setContextMenu(menu)

sys.exit(app.exec_())
