import PyQt5
from PyQt5.QtWidgets import QLabel
from demo.example_2_image.widgets.main_widget import MainWidget


def test_can_open_main_window(monkeypatch, mock_pyjapc, qtbot):
    """
    This test showcases how to check whether specific Qt operations are performed during
    your test (in this case, opening a dialog).
    The ideas is to monkey-patch the interesting operation with a lambda that throws a
    recognizable exception, and then monitor the code for such exception.
    NOTE: 'mock_pyjapc' and 'qtbot' are NOT unused parameters. They are needed to correctly perform the test.
    """
    # Define what to do if a QMessageBox tries to open
    def raise_exception_if_qmessagebox_opens():
        raise RuntimeError("A QMessageBox opened!")

    # Replace the 'exec' function of the QMessageBox with the custom function above
    monkeypatch.setattr(PyQt5.QtWidgets.QMessageBox, "exec", raise_exception_if_qmessagebox_opens)

    # No QMessageBox should open, so no RuntimeError should be thrown
    # If you expect a QMessageBox, then use 'with pytest.raises(RuntimeException):' to catch the exception
    main_widget = MainWidget()
    main_widget.show()
    assert main_widget is not None


def test_view_contains_all_the_labels(main_widget, mock_pyjapc, qtbot):

    # Does it contain all the labels?
    assert main_widget.findChild(QLabel, "title") is not None
    assert main_widget.findChild(QLabel, "subtitle") is not None
    assert main_widget.findChild(QLabel, "cern_logo") is not None
