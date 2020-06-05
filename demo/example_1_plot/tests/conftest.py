import pytest
import pyjapc

from demo.example_1_plot.widgets.main_widget import MainWidget
from demo.papc_setup.papc_devices import setup_papc_devices


@pytest.fixture()
def main_widget(qtbot):
    """
    This fixture returns a properly setup instance of your GUI,
    ready to be manipulated with qtbot.
    It will be available in your tests as 'main_widget'
    (change the function name to change this)
    """
    main_widget = MainWidget()
    main_widget.show()
    qtbot.addWidget(main_widget)
    yield main_widget


@pytest.fixture(autouse=True)
def mock_pyjapc(monkeypatch):
    """
    This fixture intercepts PyJapc calls and redirects them to a papc instance.
    Make sure you setup papc to simulate the same devices your GUI usually
    connects to.
    This fixture will make an object called 'mock_pyjapc' available in your tests
    without the need to isntantiate it.
    """
    # Monkey-patch PyJapc
    pyjapc.PyJapc = setup_papc_devices()
    japc = pyjapc.PyJapc()
    japc.setSelector("")
    # Run test
    yield japc
    # Clean up
    pyjapc.PyJapc = None

