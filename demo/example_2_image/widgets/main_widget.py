from PyQt5.QtWidgets import QWidget

# No need to import a model: this view is static.

# Import the code generated from the view.ui file
from demo.example_2_image.resources.generated.ui_view import Ui_Form


class MainWidget(QWidget, Ui_Form):
    """
        This widget is static: it loads only a View, but no model.

        This structure is useful when you have a view that does nothing but display
        something like immutable text of images.
    """
    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

        # Instantiate the view
        self.setupUi(self)