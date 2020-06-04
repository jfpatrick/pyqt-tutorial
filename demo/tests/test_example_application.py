import PyQt5
from PyQt5.QtWidgets import QPushButton, QSpinBox
from accwidgets.graph import ScrollingPlotWidget
from demo.widgets.example_widget import ExampleWidget


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
    my_gui = ExampleWidget()
    my_gui.show()
    assert my_gui is not None


def test_main_window_has_all_tabs(my_gui):
    """ Make sure the example application has all the expected tabs in the right order. """
    assert my_gui.count() == 3
    assert my_gui.tabText(0) == "Scrolling Plot"
    assert my_gui.tabText(1) == "Cyclic Plot"
    assert my_gui.tabText(2) == "Image"


def test_scrolling_plot_tab(my_gui, mock_pyjapc, qtbot):
    """ Test the scrolling plot tab looks right and does what it's expected to do. """

    # Does it contain a ScrollingPlotWidget?
    assert my_gui.scrolling_plot_tab.findChild(ScrollingPlotWidget) is not None

    # Does it contain a QSpinBox called 'amplitude_sin'?
    ampl_spinbox = my_gui.scrolling_plot_tab.findChild(QSpinBox, "amplitude_sin")
    assert ampl_spinbox is not None

    # Does it set the right value on the right device?
    ampl_spinbox.clear()
    qtbot.keyClicks(ampl_spinbox, "50")
    assert mock_pyjapc.getParam("TEST_DEVICE/Settings#amplitude_sin") == 50

    # Does it contain a QSpinBox called 'period_sin'?
    per_spinbox = my_gui.scrolling_plot_tab.findChild(QSpinBox, "period_sin")
    assert per_spinbox is not None

    # Does it set the right value on the right device?
    per_spinbox.clear()
    qtbot.keyClicks(per_spinbox, "30")
    assert mock_pyjapc.getParam("TEST_DEVICE/Settings#period_sin") == 30
