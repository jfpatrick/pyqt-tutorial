.. index:: Advanced Topics
.. _advanced_topics

===============
Advanced Topics
===============

.. index:: Compiling ``.ui`` files
.. _adv_compile_ui

Compiling .ui files
===================
Qt Designer's ``.ui`` files cannot be used directly by a PyQt application: they have to be first compiled into Python
code, and then imported properly.

The base template provided by ``bipy-gui-manager`` is already setup tp recompile your ``.ui`` files every time they
get modified: in fact most used do not have to care about these steps at all. Here is however an overview of what
is happening behind the scenes.

.. warning:: Never edit the generated files, and keep the ``.ui`` files as your primary reference. Also pushing them
    to GitLab is discouraged.

Automatic .ui Recompilation with pyqt5ac
----------------------------------------
``pyqt5ac`` is a small Python library that takes care of monitoring your ``.ui`` and ``.qrc`` files for changes and
recompile them when needed. You can see the source code `here <https://github.com/addisonElliott/pyqt5ac>`_.

In the template, the code performing this operation is the main module's ``__init__.py`` and consists of one line::

    pyqt5ac.main(config=os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pyqt5ac.yml'))

In turn, this line tells ``pyqt5ac`` to look for instructions into the ``pyqt5ac.yml`` file, hosted in the same
directory.

To know more about how to modify or deubg such file, please refer to the
`pyqt5ac documentation <https://github.com/addisonElliott/pyqt5ac>`_.

Manual compilation of ``.ui`` files
-----------------------------------
If for any reason you can't use ``pyqt5ac``, you can always compile the various files manually.

This is done in the console by issuing the following command::

    pyuic5 my_interface.ui -o my_interface_ui.py

This will generate a Python file containing a single, large class named  ``Ui_<something>``  with the complete
definition of your GUI.

Writing Resource files (.qrc)
-----------------------------
If you're not using Qt Designer, please refer to `this document <https://doc.qt.io/qt-5/resources.html>`_
to learn more about how to write resource files.


Manual compilation of ``.ui`` and ``.qrc`` files
------------------------------------------------

If you have ``.qrc`` files as well, you should always compile them first with this command::

    pyrcc5 -o resources_rc.py resources.qrc

and then recompile the ``.ui`` files with the ``--from-imports`` flag::

    pyuic5 --from-imports my_interface.ui -o my_interface_ui.py


Use ComRAD as a debug tool
~~~~~~~~~~~~~~~~~~~~~~~~~~
While you develop your interface in Qt Designer, you have only a static view of your interface, and it might be
a bit hard to figure out how does it behave in complex scenarios. In order to try it out, instead of compiling
into ``.py`` files every time, you can try to load it in
`ComRAD < https://acc-py.web.cern.ch/gitlab/acc-co/accsoft/gui/rad/accsoft-gui-rad-comrad/docs/stable/index.html>`_
for a live preview with some mock data.
