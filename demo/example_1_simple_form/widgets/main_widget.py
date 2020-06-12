from PyQt5.QtCore import pyqtSlot
from PyQt5.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel

# Import the code generated from the view.ui file
from demo.example_1_simple_form.widgets.resources import Ui_Form


class MainWidget(QWidget, Ui_Form):
    """
        This is the main class defining your GUI, also called the View.

        Signals and slots are usually connected in this class.
        The model will usually emit signal which are catch either directly
        by the View, or by this class, which translates them into operations
        on the View.
    """
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        # Instantiate the view
        self.setupUi(self)

        # Find the Send Message button
        send_button = self.findChild(QPushButton, "sendMessage_btn")

        # When clicked, set the Label content to the TextBox content
        send_button.clicked.connect(self.send_message)

    @pyqtSlot()
    def send_message(self):
        text_editor = self.findChild(QLineEdit, "messageEditor_txt")
        message_display = self.findChild(QLabel, "messageDisplay_lbl")
        message_display.setText(text_editor.text())
