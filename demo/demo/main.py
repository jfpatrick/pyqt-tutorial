import sys
import logging

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox
from be_bi_application_frame.application_frame import ApplicationFrame

# Import the Presenter from the widgets folder
from demo.widgets.example_widget import ExampleWidget
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
    window = ApplicationFrame()

    try:
        # Instantiate your GUI (here the ExampleWidget class)
        example_widget = ExampleWidget(parent=window)

        # Apply small customizations to the application (window title, window icon...)
        example_widget.setWindowIcon(QIcon('resources/images/CERN_logo.png'))

        # Add the example widget to the window
        window.setCentralWidget(example_widget)

        # Set the window title
        window.setWindowTitle(APPLICATION_NAME)

    except Exception as e:

        # If something goes wrong, shows a small QDialog with an error message and quits
        dialog = QMessageBox()
        dialog.critical(window, "Error", "An Exception occurred at startup:\n\n{}\n\n".format(e) +
                                         "See the logs for more information, " +
                                         "and please report this issue to {} ({})".format(AUTHOR, EMAIL))
        window.deleteLater()
        return

    # Enter the event loop by showing the window
    window.show()

    # Once left the event loop, terminates the application
    sys.exit(app.exec_())
