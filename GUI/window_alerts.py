from PyQt5.QtWidgets import QMessageBox

from managers.settings import to_default_values


def restore_alert(parent):
    reply = QMessageBox.warning(parent, 'Restore Defaults',
                                'Are you sure you want to restore preferences to default values?'
                                '\nAll made changes will be lost.',
                                QMessageBox.RestoreDefaults | QMessageBox.Cancel, QMessageBox.Cancel)
    if reply == QMessageBox.RestoreDefaults:
        to_default_values()
        parent.print_console('Preferences restored succesfully.', "QLabel { color : darkblue; }")


def close_alert(parent, event):
    reply = QMessageBox.critical(parent, 'Quit', 'Are you sure you want to quit?\nThe program is still running.',
                                 QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
    if reply == QMessageBox.Yes:
        parent.robot.stop = True
        parent.robot.join(0.1)
        event.accept()
    else:
        event.ignore()
