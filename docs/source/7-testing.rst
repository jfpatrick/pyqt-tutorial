.. index:: Testing and Linting
.. _testing_linting:

===================
Testing and Linting
===================

Testing and linting are two important practices to ensure code quality over time and minimize technical debt.

Here we overview the tools available to automate these two tasks effectively with Acc-Py and GitLab CI.


.. index:: Linting
.. _linting:

Linting
=======

.. warning:: This section is incomplete.

Linting is the process of automatically checking your Python code for typos, bugs and code smells.

It is usually done through linters like ``mypy`` or ``flake``. Both of these tools are already configured by Acc-Py:
you can run them by typing::

    acc-py check




.. index:: Testing
.. _testing:

Testing
=======
Testing allows you to quickly track down the source of new bugs, and in general reduces maintenance costs in the
long term. Testing PyQt applications can be done on two levels:

 * **unit testing** (white-box testing, function-level testing) or
 * **acceptance testing** (black-box testing, graphical-level testing).

If your application interacts with the control system, you will also have to mock those interactions either with
``MagicMock`` or by simulating the underlying layer with ``papc``.

.. note:: ``papc`` is better suited for complex test scenarios and requires a good amount of coding.
    It's therefore considered a more advanced way of testing and it is covered in a
    :doc:`separate section <89-papc>`.


.. index:: Unit Tests with pytest
.. _unit_tests:
.. _pytest:

Simple unit tests - pytest
--------------------------
These can be performed on all the functions that do not belong to any PyQt widget or PyQt's ``QObject``, and don't talk
to the control system. It boils down to regular Python testing, for which there are multiple
`resources <https://docs.pytest.org/en/latest/talks.html>`_ available on the Internet.

.. note:: ``pytest`` is already setup with Acc-Py, so no installation or setup is required. You only have to
    remember to add it to your dependencies in ``setup.py``. Once done, it's enough to place your unit tests
    in the ``tests/`` folder and type::

        python -m pytest

    to execute them.

.. warning:: All Python files containing tests must start with the prefix ``test_`` in order to be found by ``pytest``
    and executed. For example ``test_my_app.py`` will be found and run, ``TestMyApp.py`` won't.

``pytest`` has a number of interesting options and plugins. The most interesting ones for unit tests are the following:

 * **Verbosity**:

    - ``-vv`` increases pytests' own log level to the maximum verbosity.
    - ``--log-cli-level=DEBUG`` displays the logs from your application down to the level specified
      (in the example, ``DEBUG``).

 * **pytest-cov**: package that provides a coverage report of your tests. Add ``pytest-cov`` to your ``setup.py``
   and the flag ``--cov=<project_name>`` to the ``pytest`` call. See the
   `docs <https://pytest-cov.readthedocs.io/en/latest/readme.html>`_.

 * **pytest-random-order**: package that randomizes your tests, to ensure they don't influence each other.
   Add ``pytest-random-order`` to your ``setup.py`` and the flag ``--random-order`` to your ``pytest`` call.
   See the `docs <https://github.com/jbasko/pytest-random-order/blob/master/README.rst>`_.

Remember to read the `pytest documentation <https://docs.pytest.org/en/latest/contents.html>`_ or a good
`tutorial <https://realpython.com/pytest-python-testing/>`_ before starting, and to leverage its features, like
`fixtures <https://docs.pytest.org/en/latest/fixture.html>`_, to keep your code tidy,
setup and tear down tests, and mock bigger components of your application.


.. index:: Mocking the Control System API
.. _mocking:

Unit tests on the control system's API
--------------------------------------
Special attention is required if you want to perform tests on some functions that interact with the control system,
but at the same time you don't want the interaction to happen for real (for example, to avoid having to reset your
device every time you run a test, or if your app is interacting with operational devices).

Testing can be done successfully (and meaningfully) by
`mocking the control system's API <https://en.wikipedia.org/wiki/Mock_object>`_.
This can be done on different levels:

 * With a ``Mock`` object from the ``unittest`` package: use this if you just want to be able to instantiate a
   class that internally connects to the control system, but does not need to get/set any data from them for the test.
   See the `documentation <https://docs.python.org/3.6/library/unittest.mock.html>`_ for examples and more information.

 * With a ``MagicMock`` object from the ``unittest`` package: use this if you want to be able to get/set
   data on the control system, but you need only to make sure the get/set is done with the correct data,
   not that it actually has the desired effect on the device. See the
   `documentation <https://docs.python.org/3.6/library/unittest.mock.html>`_ for examples and more information.

 * With ``papc``: use this for more complex use cases where you need a full-blown simulation of your target devices
   in the control system (like testing the overall application behavior to a sequence of device states).
   Requires more work than the previous two. See the :doc:`dedicated page <89-papc>`.


.. index:: Mocking PyJAPC
.. _mocking_pyjapc:

Example: Mocking PyJAPC
---------------------------
This fixture will monkey-patch PyJAPC objects by replacing them with a mock of your choice::

    # autouse=True is optional: means that this fixture is applied to all the tests
    @pytest.fixture(autouse=True)
    def mock_pyjapc():

        # Execute this part before the test
        # From now, calling pyjapc.PyJapc() will not instantiate a PyJapc() object,
        # but a Mock() / MagicMock() / papc object instead, without your app noticing.
        pyjapc.PyJapc = <Mock(), MagicMock(), or your papc-simulated PyJapc object>

        logging.debug("pyjapc.PyJapc has been replaced by {}".format(pyjapc.PyJapc))

        # Execute the test
        yield

        # Execute this part after the test
        # Important to avoid memory leaks, especially with papc
        pyjapc.PyJapc = None

    def test_myapp_thinks_it_can_use_pyjapc(mock_pyjapc):

        # Now this function will not fail even if it cannot access the control system.
        my_app.function_instantiating_PyJapc_objects()

        # Now this function will not actually set anything, but it will not fail.
        my_app.function_setting_values_to_some_device("some value")


Passing such fixture as an argument to your test, your application's ``pyjapc.PyJapc`` class will be automagically
replaced by the mock without having to modify any code in the target app.

The same thing can be done with functions, object's functions, etc.
See the `documentation <https://docs.pytest.org/en/latest/monkeypatch.html>`_
for more examples of monkey-patching that might work better for your use-case,
and the ``Mock()`` and ``MagicMock()`` `documentation <https://docs.python.org/3.6/library/unittest.mock.html>`_
for more examples.


.. index:: Graphical Tests with ``pytest-qt``
.. index:: Acceptance Tests with ``pytest-qt``
.. index:: ``pytest-qt``
.. _pytest_qt:

Graphical acceptance tests
--------------------------
Running graphical acceptance tests is surprisingly easy, even though slightly fragile.

You need to install the ``pytest-qt`` package and basically
`follow its documentation <https://pytest-qt.readthedocs.io/en/latest/tutorial.html>`_.

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



.. index:: Troubleshooting Tests
.. _troubleshoot_tests:

Troubleshooting
-------------------------

.. index:: Abort()
.. _qt_abort:

Qt throws Abort() during the tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you installed ``pytest-xvfb``, please remove it and try again.
Otherwise, make sure you're passing your Qt objects to ``qtbot`` with ``qtbot.addWidget(my_widget)``
before trying to perform any operation on it.

.. index:: Tests never start
.. _tests_hang:

The tests hang forever while trying to start
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It might be trying to communicate with the control system. This error is likely to happen in GitLab CI
because its runners are *not* TN-trusted, so it will fail.

Verify which part of your application is trying to contact the control system and mock it in a meaningful way.
See the `above paragraph <7-testing.html#mocking>`_ on testing control system APIs.

.. index:: "Failed to connect to all InCA servers"
.. _failed_to_connect:

The tests fail with "Failed to connect to all InCA servers"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Full error is::

    jpype._jclass.org.springframework.remoting.RemoteAccessException:
    org.springframework.remoting.RemoteAccessException: Failed to connect to all InCA servers

Same as above: your app is probably trying to contact the control system. Mock the relative function/object.
See the `above paragraph <7-testing.html#mocking>`_ on testing control system APIs.



.. index:: Testing and Linting FAQ
.. _testing_faq:

FAQ
===

*TODO*
