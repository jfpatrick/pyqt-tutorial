import os
import sys
import logging

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget

# Import the Presenter from the widgets folder
from demo.example_2_image.widgets.main_widget import MainWidget
from demo.constants import APPLICATION_NAME, AUTHOR, EMAIL


def main():
    """
        Application's entry point. It instantiates the QApplication, the main window
        and the ApplicationFrame widgets, that will contain your GUI.
        Then loads your widgets into the main windows and shows it, entering the event loop.
    """
    logging.info("Starting up {}...".format(APPLICATION_NAME))

    # Instantiate the QApplication and the ApplicationFrame
    app = QApplication(sys.argv)

    try:
        # Instantiate your GUI
        widget = MainWidget()

        # Set window icon
        icon_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '../window_icon.png')
        widget.setWindowIcon(QIcon(icon_path))

    except Exception as e:

        # If something goes wrong, shows a small QDialog with an error message and quits
        widget = QWidget()
        dialog = QMessageBox()
        dialog.critical(widget, "Error", "An Exception occurred at startup:\n\n{}\n\n".format(e) +
                                         "See the logs for more information, " +
                                         "and please report this issue to {} ({})".format(AUTHOR, EMAIL))
        widget.deleteLater()
        return

    # Enter the event loop by showing the window
    widget.show()

    # Once left the event loop, terminates the application
    sys.exit(app.exec_())
