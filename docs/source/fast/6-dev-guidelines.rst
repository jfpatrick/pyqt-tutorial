.. index:: Development Guidelines
.. _dev_guidelines

======================
Development Guidelines
======================

.. index:: Testing
.. _testing

Testing
=======
Testing allows you to quickly track down the source of new bugs, and in general reduces maintenance costs in the
long term. Testing PyQt applications can be done on two levels:

 * **unit testing** (white-box testing, function-level testing) or
 * **acceptance testing** (black-box testing, graphical-level testing).

If your application interacts with the control system, you will also have to mock those interactions either with
``MagicMock`` or by simulating the underlying layer with ``papc``.


.. index:: Unit Tests with pytest
.. _unit_tests
.. _pytest

Simple unit tests - pytest
--------------------------
These can be performed on all the functions that do not belong to any PyQt widget or PyQt's QObject, and don't talk
to the control system. It boils down to regular Python testing, for which there are multiple tutorials available on
the Internet.

.. note:: ``pytest`` is already setup with Acc-Py: so it's enough to place your unit tests in the ``tests/``
    folder and then call::

        python -m pytest

.. note:: All Python files containing tests must start with the prefix ``test_`` in order to be found by ``pytest``
    and executed. For example ``test_my_app.py`` will be found and run, ``TestMyApp.py`` won't.

``pytest`` has a number of interesting options and plugins. The most interesting ones for unit tests are the following:

 * **Verbosity**:

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


.. index:: Mocking the Control System API
.. _mocking

Unit tests on the control system's API
--------------------------------------
Special attention is required if you want to perform tests on some functions that interact with the control system,
but at the same time you don't want the interaction to happen for real (for example, to avoid having to reset your
device every time you run a test, or if your app is interacting with operational devices).

Testing can be done successfully (and meaningfully) by
`mocking the control system's API <https://en.wikipedia.org/wiki/Mock_object>`_.
This can be done on different levels:

 * With a ``Mock`` object from the ``unittest`` package

   Useful for somebody who just want to be able to instantiate a class that connects to the control system, but
   does not need to get/set any data from them for the test.
   See the `documentation <https://docs.python.org/3.6/library/unittest.mock.html>`_ for examples and more information.

 * With a ``MagicMock`` object from the ``unittest`` package

   Useful for somebody who wants to be able to get/set data on the control system, but needs only to make sure
   the get/set is done with the correct data, not that it actually has the desired effect on the device.
   See the `documentation <https://docs.python.org/3.6/library/unittest.mock.html>`_ for examples and more information.

 * With ``papc``

   For more complex use cases where you need a full-blown simulation of your target devices in the control system.
   Requires more work than the previous two. See the `dedicated section <#>`_.


.. index:: Mocking PyJAPC
.. _mocking_pyjapc

Example: Mocking PyJapc
-----------------------
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

The same thing can be done with functions, object's functions, etc.
See the `documentation <https://docs.pytest.org/en/latest/monkeypatch.html>`_
for more examples of monkey-patching that might work better for your use-case,
and the ``Mock()`` and ``MagicMock()`` `documentation <https://docs.python.org/3.6/library/unittest.mock.html>`_
for examples.

Passing such fixture as an argument to your test, your application's ``pyjapc.PyJapc`` class will be automagically
replaced by the mock without having to modify any code.


.. index:: Graphical Tests with ``pytest-qt``
.. _graphical_tests
.. _acceptance_tests
.. _pytest_qt

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


.. index:: Linting
.. _linting

Linting
=======
*TODO*


.. index:: GUI Design Strategies
.. _gui_design

GUI Design
==========
PyQt5 allows for two strategies for designing GUIs: either with the Qt Designer, which generates XML ``.ui`` files,
or through code, in ``.py`` files.

In general, for complex applications, it is recommended to design the interface with Qt Designer.
However, in special cases it might be more convenient to use only code: in the end it's up to you to decide what
is the more sensible approach for your specific case.


.. index:: Qt Designer files
.. index:: .ui files
.. _ui_files

Design with Qt Designer (using .ui files)
-----------------------------------------
You can design your PyQt GUI by using the Qt Designer.

The version shipped with Acc-Py is basically identical to any vanilla Qt Designer, so any good
`tutorial <https://doc.qt.io/qt-5/qtdesigner-manual.html>`_ on the Internet should be valid.
The only addition of Acc-Py version is the presence of some extra CERN specific widgets,
which you can add to your app just like regular Qt widgets.

Once you finished your design, you will end up with one or more XML ``.ui`` files.
These files cannot be loaded directly in a PyQt application (unlike QML files), but have to be compiled.

.. warning:: QML files are **not recommended** and **not supported** by Acc-Py's team or by BI, due to its
    remarkably poor plotting performance.

.. note:: The compilation can be done automatically, but also manually. if you are using the boilerplate code from
    ``bipy-gui-manager``, the automatic compilation is already setup for you. If you want to know the details of how
    it works, or you need to compile manually, check `this page <#>`_.


.. index:: Using .ui files
.. index:: .ui files usage
.. _ui_files_usage

Using the .ui files in code
---------------------------
Once you created your interface, you can load the interface into your application.

The loading is done into the Presenter, that is, into any file in the ``widgets`` folder::

    import sys
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtWidgets import QApplication
    from my_app.main_window import Ui_MyMainWindow

    class ExampleWidget(QtWidgets.QMainWindow, Ui_MyMainWindow):
        def __init__(self, parent=None):
            super(MyAppGui, self).__init__(parent)
            self.setupUi(self)

.. note:: Some older PyQt tutorials recommend loading the Ui in another, equally valid way, which is the following::

            import sys
            from PyQt5 import QtCore, QtGui, QtWidgets
            from PyQt5.QtWidgets import QApplication
            from my_app.main_window import Ui_MyMainWindow

            class MyAppGui(QtWidgets.QMainWindow):
                def __init__(self, parent=None):
                    QtWidgets.QMainWindow.__init__(self, parent)
                    self.ui = Ui_MyMainWindow()
                    self.ui.setupUi(self)

    This loads the Ui by instantiating it as an attribute of your main window. It's an old-fashioned,
    PyQt4-style, but works.


.. index:: Design GUI in code
.. _gui_py_files

Design in code
--------------
If you have very specific use cases, or your application is made mostly of reusable widgets that don't come from
``accwidgets`` (thus not available in Qt Designer), you might want to build up you interface directly in code.
From this regard, there are no limitations in what you can do: just follow some good tutorial on how to deal with
``QMainWindow`` and Qt's layouts before jumping in.

In addition, you can still use ``accwidgets``' components by importing it (remember to add ``accwidgets``
in the core dependencies of your ``setup.py``). It's still recommended, where it makes sense, to isolate the
layouting code from the wiring (signal/slots) and from the rest of the application's logic.

So please don't write your entire GUI as a single file, unless is nothing more than a quick experiment.


.. index:: Resource Files (.qrc)
.. index:: .qrc files
.. _qrc_files

Resource files (.qrc)
---------------------
If you're adding static resources to your interface (like images, custom icons, etc..) you have to use a
**resource file (.qrc)**.

If you are using Qt Designer, the procedure goes as follow:

 * Add a new resource file by clicking on the wrench icon on the ``Select Resource`` dialog
   (opened, for example, by trying to add an icon to a Window).

 * Create a new file in the folder of your resources, named for example ``resources.qrc``

 * Add the path to your icon/image in such file, still using the dialog.

 * Put your icons/images where you need and save your ``.ui`` file.

 * If your Designer files are compiled automatically, your ``.qrc`` file will be automatically detected and compiled
   as soon as you start your application. If not, check out `the advanced topics page <#>`_
   to know more about how to compile these files manually.

 * You can now launch the application and make sure it runs. After the first run,
   you should see a file called ``resources_rc.py`` among your generated ``ui_*.py`` files.


.. index:: Continuous Integration
.. index:: GitLab CI
.. _gitlab_ci

Continuous Integration (CI)
============================

GitLab CI is a powerful tool to ensure the code you publish on GitLab works as expected.
It's a pipeline that sets up a virtual machine and runs a number of operations on your code, namely running tests,
linting, producing coverage reports, and many more.

It is mostly setup already by the Acc-Py team, and some extra customizations are added by ``bipy-gui-manager``.
To learn more about the nature of such modifications, check out the `.gitlab-ci.yml` file description
`here <LINK HERE>`_.

.. index:: GitLab CI Troubleshooting
.. _gitlab_ci_troubleshoot

Troubleshooting
---------------

.. index:: Abort()
.. _qt_abort

Qt throws Abort() during the tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
If you installed ``pytest-xvfb`` on your GitLab CI image, please remove it and try again.
Otherwise, make sure you're passing your Qt objects to ``qtbot`` with ``qtbot.addWidget(my_widget)``
 before trying to perform any operation on it.

.. index:: CI pipeline never starts
.. _pipeline_hangs

The pipeline hangs forever while trying to start the tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
It might be trying to communicate with the control system: GitLab CI is *not* TN-trusted, so it will fail.
Verify which part of your application is trying to contact the control system and mock it in a meaningful way.
See the above paragraph on testing control system APIs.

.. index:: "Failed to connect to all InCA servers"
.. _failed_to_connect

The pipeline fails with an error saying "Failed to connect to all InCA servers"
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Full error is: ``jpype._jclass.org.springframework.remoting.RemoteAccessException: org.springframework.remoting.RemoteAccessException: Failed to connect to all InCA servers``.

Same as above: your app is probably trying to contact the control system. Mock the relative function/object.
See the above paragraph on testing control system APIs.

Tips and Tricks
---------------

Add coverage badge
~~~~~~~~~~~~~~~~~~~
In GitLab's side bar, press ``Settings > General > Badges``. The fill the fields as follows::

    Name: coverage
    Link: https://gitlab.cern.ch/<user or group>/<my_app>/pipelines
    Badge image URL: https://gitlab.cern.ch/<user or group>/<my_app>/badges/master/coverage.svg

The next time a pipeline runs on master, the number should be updated.

Make screenshot during the tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*TODO Check Acc_py documentation*
