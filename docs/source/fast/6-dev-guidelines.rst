Development Guidelines
-----------------------

Testing
^^^^^^^
Testing allows you to quickly track down the source of new bugs, and in general reduces maintenance costs in the
long term. Testing PyQt applications can be done on two levels:

 * **unit testing** (white-box testing, function-level testing) or
 * **acceptance testing** (black-box testing, graphical-level testing).

If your application interacts with the control system, you will also have to mock those interactions either with
``MagicMock`` or by simulating the underlying layer with ``papc``.

Simple unit tests - pytest
~~~~~~~~~~~~~~~~~~~~~~~~~~
These can be performed on all the functions that do not belong to any PyQt widget or PyQt's QObject, and don't talk
to the control system. It boils down to regular Python testing, for which there are multiple tutorials available on
the Internet.

.. note:: ``pytest`` is already setup with Acc-Py: so it's enough to place your unit tests in the ``tests/``
    folder and then call::

        python -m pytest

.. note:: All Python files containing tests must start with the prefix ``test_`` in order to be found by ``pytest``
    and executed. For example ``test_my_app.py`` will be found and run, ``TestMyApp.py`` won't.

``pytest`` has a number of interesting options and plugins. The most interesting ones for unit tests are the following:

 * **Verbosity settings**:
    - ``-vv`` increases pytests' own log level to the maximum verbosity.
    - ``--log-cli-level=DEBUG`` displays the logs from your application down to the level specified
      (in the example, ``DEBUG``).

 * **pytest-cov**: package that provides a coverage report of your tests. Add ``pytest-cov`` to your ``setup.py``
   and the flag ``--cov=my_app`` to the ``pytest`` call. See the
   `docs <https://pytest-cov.readthedocs.io/en/latest/readme.html>`_.

 * **pytest-random-order**: package that randomizes your tests, to ensure they don't influence each other.
   Add ``pytest-random-order`` to your ``setup.py`` and the flag ``--random-order`` to your ``pytest`` call.
   See the `docs <https://github.com/jbasko/pytest-random-order/blob/master/README.rst>`_.

Remember to read the `pytest documentation <https://docs.pytest.org/en/latest/contents.html>`_ or a good
`tutorial <https://realpython.com/pytest-python-testing/>`_ before starting and to leverage its features, like
`fixtures <https://docs.pytest.org/en/latest/fixture.html>`_, to avoid duplicating code,
setting up and tearing down tests, and to mock bigger components of your application.


Unit tests on the control system's API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Special attention is required if you want to perform tests on some functions that interact with the control system,
but at the same time you don't want the interaction to happen for real (for example, to avoid having to reset your
device every time you run a test, or if your app is interacting with operational devices).

Testing can be done successfully (and meaningfully) by mocking the control system's API.
This can be done on different levels:

 * With a ``Mock`` object from the ``unittest`` package
   Useful for somebody who just want to be able to instantiate a class that connects to the control system, but
   does not need to get/set any data from them for the test.
   See the documentation for examples and more information.

 * With a ``MagicMock`` object from the ``unittest`` package
   Useful for somebody who wants to be able to get/set data on the control system, but needs only to make sure
   the get/set is done with the correct data, not that it actually has the desired effect on the device.
   See the documentation for examples and more information.

 * With ``papc``
   For more complex use cases where you need a full-blown simulation of your target devices in the control system.
   Requires more work than the previous two. See the `dedicated section <#>`_.

Example: Mocking PyJapc
~~~~~~~~~~~~~~~~~~~~~~~
This fixture will monkey-patch PyJapc objects by replacing them with a mock of your choice::

    @pytest.fixture(autouse=True)  # autouse=True is optional: means that this fixture is applied to all the tests
    def mock_pyjapc():
        # Execute this part before the test
        pyjapc.PyJapc = <Mock(), MagicMock(), or your papc-simulated PyJapc object>  # From now, calling pyjapc.PyJapc() will not instantiate a PyJapc() object,
                                                                                     # but a Mock() / MagicMock() / papc object instead, without your app noticing.
        logging.debug("pyjapc.PyJapc has been replaced by {}".format(pyjapc.PyJapc))
        # Execute the test
        yield
        # Execute this part after the test
        pyjapc.PyJapc = None  # Important to avoid memory leaks, especially with papc

    def test_myapp_thinks_it_can_use_pyjapc(mock_pyjapc):
        my_app.function_instantiating_PyJapc_objects()
        my_app.function_setting_values_to_some_device("some value")

The same thing can be done with functions, object's functions, and the like.
See the documentation for more examples of monkey-patching that might work better for your use-case,
and the ``Mock()`` and ``MagicMock()`` documentation for examples.

Passing such fixture as an argument to your test, your application's ``pyjapc.PyJapc`` class will be automagically
replaced by the mock without having to modify any code.

Graphical acceptance tests
~~~~~~~~~~~~~~~~~~~~~~~~~~
Running graphical acceptance tests is surprisingly easy, even though slightly fragile.

You need to install the ``pytest-qt`` package and basically follow its documentation.

The core idea is that you are given an object, called ``qtbot``, that can perform clicks, scrolls, and regular
user interface operations on your GUI, while you can inspect the Python objects to see if the expected changes happen.

Here is a simple example of a graphical test::

    import pytest
    from myapp.main_window import MyMainWindow

    @pytest.fixture()
    def main_window(qtbot):
        main_window = MyMainWindow()
        main_window.show()
        qtbot.addWidget(main_window)
        return main_window

    def test_freeze_button_works(main_window, qtbot):
        assert main_window.freeze_btn.text() == "Freeze"
        qtbot.mouseClick(main_window.freeze_btn, Qt.LeftButton)
        assert main_window.freeze_btn.text() == "Unfreeze"
        qtbot.mouseClick(main_window.freeze_btn, Qt.LeftButton)
        assert main_window.freeze_btn.text() == "Freeze"

Linting
^^^^^^^
[TODO once I do it myself]
