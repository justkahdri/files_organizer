from GUI.restore_alert_ui import *
from managers.settings import to_default_values


class RestoreAlert(QtWidgets.QDialog, Ui_RestoreAlert):
    def __init__(self, parent=None, *args, **kwargs):
        QtWidgets.QDialog.__init__(self, *args, **kwargs)
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        # self.setFixedSize(420, 130)
        self.parent = parent

        self.buttonBox.clicked.connect(self.btn_resolve)

    def btn_resolve(self, s):
        message = s.text()
        if message == 'Restore Defaults':
            to_default_values()
            self.parent.print_console('Preferences restored succesfully.', "QLabel { color : darkblue; }")
        self.close()


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    window = RestoreAlert()
    window.show()
    app.exec_()
