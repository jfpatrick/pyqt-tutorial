import PyQt5
from PyQt5.QtWidgets import QPushButton, QSpinBox
from accwidgets.graph import ScrollingPlotWidget
from demo.example_1_plot.widgets.main_widget import MainWidget


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


def test_plot_exists(main_widget, mock_pyjapc, qtbot):

    # Does it contain a ScrollingPlotWidget?
    assert main_widget.findChild(ScrollingPlotWidget) is not None


def test_spinbox_works(main_widget, mock_pyjapc, qtbot):
    """ Test the scrolling plot tab looks right and does what it's expected to do. """

    # Does it contain a QSpinBox called 'amplitude_sin'?
    ampl_spinbox = main_widget.findChild(QSpinBox, "amplitude_sin")
    assert ampl_spinbox is not None

    # Does it set the right value on the right device?
    ampl_spinbox.clear()
    qtbot.keyClicks(ampl_spinbox, "50")
    assert mock_pyjapc.getParam("TEST_DEVICE/Settings#amplitude_sin") == 50

    # Does it contain a QSpinBox called 'period_sin'?
    per_spinbox = main_widget.findChild(QSpinBox, "period_sin")
    assert per_spinbox is not None

    # Does it set the right value on the right device?
    per_spinbox.clear()
    qtbot.keyClicks(per_spinbox, "30")
    assert mock_pyjapc.getParam("TEST_DEVICE/Settings#period_sin") == 30
