import os
import sys
import logging

from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QApplication, QMessageBox, QTabWidget

# Import the Presenters from the widgets folder of all the modules
from demo.example_1_simple_form.widgets.main_widget import MainWidget as Example1Widget
from demo.example_2_image.widgets.main_widget import MainWidget as Example2Widget
from demo.example_3_plot.widgets.main_widget import MainWidget as Example3Widget

# Import the constants
from demo.constants import APPLICATION_NAME, AUTHOR, EMAIL


def main():
    """
        Application's entry point. It instantiates the QApplication, the main window
        and the ApplicationFrame widgets, that will contain your GUI.
        Then loads your widgets into the main windows and shows it, entering the event loop.
    """
    logging.info("Starting up {}...".format(APPLICATION_NAME))

    # Instantiate the QApplication
    app = QApplication(sys.argv)

    # Create the tabs container
    tabs = QTabWidget()

    try:
        # Instantiate your GUIs (here all the widgets from the examples)
        widget_1 = Example1Widget()
        widget_2 = Example2Widget()
        widget_3 = Example3Widget()

        # Add the widgets to the window as tabs
        tabs.addTab(widget_1, QIcon(), "Example 1 - Simple Form")
        tabs.addTab(widget_2, QIcon(), "Example 2 - Image")
        tabs.addTab(widget_3, QIcon(), "Example 3 - Plot")

        # Set the window title
        tabs.setWindowTitle(APPLICATION_NAME)

        # Set window icon
        icon_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'window_icon.png')
        tabs.setWindowIcon(QIcon(icon_path))

    except Exception as e:

        # If something goes wrong, shows a small QDialog with an error message and quits
        dialog = QMessageBox()
        dialog.critical(tabs, "Error", "An Exception occurred at startup:\n\n{}\n\n".format(e) +
                                       "See the logs for more information, " +
                                       "and please report this issue to {} ({})".format(AUTHOR, EMAIL))
        tabs.deleteLater()
        return

    # Enter the event loop by showing the window
    tabs.show()

    # Once left the event loop, terminates the application
    sys.exit(app.exec_())
