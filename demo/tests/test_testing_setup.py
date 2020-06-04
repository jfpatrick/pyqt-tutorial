import pyjapc

from PyQt5.QtWidgets import QTabWidget
from PyQt5.QtGui import QIcon


def test_can_use_qt(qtbot):
    """
    Makes sure there are no problems with Qt in general.
    Unrelated to the actual application.
    """
    class TestWindow(QTabWidget):
        def __init__(self, parent=None):
            super(TestWindow, self).__init__(parent)
            self.resize(1366, 900)
            self.setWindowTitle("Test Window")
            self.setWindowIcon(QIcon('resources/images/CERN_logo.png'))

    main_window = TestWindow()
    main_window.show()
    qtbot.addWidget(main_window)
    assert main_window is not None


def test_can_use_pyjapc():
    """
    Makes sure there are no problems mocking PyJapc with papc.
    Unrelated to the actual application.
    """
    japc_ppm = pyjapc.PyJapc()
    # Make sure these selectors and properties and fields are available in the mocked devices,
    # otherwise change them.
    japc_ppm.setSelector(timingSelector="")
    japc_ppm.setParam("BISWRef1/Settings", {'frequency': 1})
    value = japc_ppm.getParam("BISWRef1/Settings#frequency")
    assert value is not None
    assert value == 1


def test_can_use_pyjapc_within_qt(qtbot):
    """
    Makes sure there are no problems with mocking PyJapc within a Qt application.
    Unrelated to the actual application.
    """
    class TestWindow(QTabWidget):
        def __init__(self, parent=None):
            super(TestWindow, self).__init__(parent)
            self.resize(1366, 900)
            test_can_use_pyjapc()
            self.setWindowTitle("Test Window")

    main_window = TestWindow()
    main_window.show()
    qtbot.addWidget(main_window)
    assert main_window is not None
    assert main_window.windowTitle() == "Test Window"
