from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
import sys

from settings import load_preferences

class MainWindow(QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setWindowTitle("Files Organizer 2.0")

        label = QLabel("WELCOME TO THE FILES ORGANIZER")
        label.setAlignment(Qt.AlignCenter)
        self.setCentralWidget(label)

        toolbar = QToolBar("Main toolbar")
        toolbar.setIconSize(QSize(16, 16))
        # toolbar.setToolButtonStyle(Qt.ToolButtonTextBesideIcon)
        self.addToolBar(toolbar)

        info_button = QAction(QIcon("icons/information.png"), "Log Status", self)
        info_button.setStatusTip("Shows the current configuration")
        info_button.triggered.connect(self.display_info)
        toolbar.addAction(info_button)

        toolbar.addWidget(QLabel("Group Files"))
        toolbar.addWidget(QCheckBox())

        toolbar.addSeparator()

        observer_button = QAction(QIcon("icons/control.png"), "Start Observer", self)
        observer_button.setStatusTip("Starts the files organizer")
        observer_button.triggered.connect(self.onMyToolBarButtonClick)
        observer_button.setCheckable(True)
        toolbar.addAction(observer_button)

        self.setStatusBar(QStatusBar(self))

    def onMyToolBarButtonClick(self, s):
        print("click", s)

    def display_info(self, s):
        layout = QVBoxLayout()
        info = load_preferences()

        path = QLabel(f"Currently checking {info['search-path']}")
        filetypes = QLabel(f'Looking for the following filetypes: {", ".join(info["extensions"])}')
        filetypes.setAlignment(Qt.AlignLeft | Qt.AlignBottom)
        if info["group-files"]["active"]:
            group = QLabel(f'Files will be grouped in "{info["group-files"]["folder"]}" folder')
        else:
            group = QLabel('Grouping files is disabled')

        widgets = [path, filetypes, group]

        for w in widgets:
            layout.addWidget(w)

        widget = QWidget()
        widget.setLayout(layout)
        self.setCentralWidget(widget)


app = QApplication(sys.argv)

if __name__ == '__main__':
    window = MainWindow()
    window.show() # Windows are hidden by default

    app.exec_()
