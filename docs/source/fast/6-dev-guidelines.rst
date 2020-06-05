.. index:: Development Guidelines
.. _dev_guidelines:

======================
Development Guidelines
======================


.. index:: GUI Design Strategies
.. _gui_design:

GUI Design
==========
PyQt5 allows for two strategies for designing GUIs: either with the Qt Designer, which generates XML ``.ui`` files,
or through code, in ``.py`` files.

In general, for complex applications, it is recommended to design the interface with Qt Designer.
However, in special cases it might be more convenient to use only code: in the end it's up to you to decide what
is the more sensible approach for your specific case.


.. index:: Qt Designer files
.. index:: .ui files
.. _ui_files:

Design with Qt Designer (using ``.ui`` files)
-----------------------------------------
You can design your PyQt GUI by using the `Qt Designer <https://doc.qt.io/qt-5/qtdesigner-manual.html>`_.

The version shipped with Acc-Py is basically identical to any vanilla Qt Designer, so any good
`tutorial <https://relentlesscoding.com/2017/08/25/tutorial-rapid-gui-development-with-qt-designer-and-pyqt/#installation>`_
on the Internet should be valid.
The only addition of Acc-Py version is the presence of some extra CERN specific widgets,
which you can add to your app just like regular Qt widgets.

Once you finished your design, you will end up with one or more XML ``.ui`` files.
These files cannot be loaded directly in a PyQt application (unlike QML files), but have to be compiled.

.. warning:: QML files are **not recommended** and **not supported** by Acc-Py's team or by BI, due to its
    remarkably poor plotting performance.

.. note:: The compilation can be done automatically, but also manually. if you are using the boilerplate code from
    ``bipy-gui-manager``, the automatic compilation is already setup for you. If you want to know the details of how
    it works, or you need to compile manually, check `this page <#>`_.


.. index:: Using ``.ui`` files
.. index:: ``.ui`` files usage
.. _ui_files_usage:

Using the ``.ui`` files in code
-------------------------------
Once you created your interface, you can load the interface into your application.

The loading is done into the Presenter, that is, into any file in the ``widgets`` folder::

    import sys
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtWidgets import QApplication
    from my_app.generated.main_window import Ui_Form

    class ExampleWidget(QtWidgets.QMainWindow, Ui_Form):
        def __init__(self, parent=None):
            super(MyAppGui, self).__init__(parent)
            self.setupUi(self)

.. note:: Some older PyQt tutorials recommend loading the Ui in another equally valid way, which is the following::

            import sys
            from PyQt5 import QtCore, QtGui, QtWidgets
            from PyQt5.QtWidgets import QApplication
            from my_app.generated.main_window import Ui_Form

            class MyAppGui(QtWidgets.QMainWindow):
                def __init__(self, parent=None):
                    QtWidgets.QMainWindow.__init__(self, parent)
                    self.ui = Ui_Form()
                    self.ui.setupUi(self)

    This loads the Ui by instantiating it as an attribute of your main window. It's an old-fashioned,
    PyQt4-style, but works just fine.


.. index:: Design GUI in code
.. _gui_py_files:

Design in code
--------------
If you have very specific use cases, or your application is made mostly of reusable widgets that don't come from
``accwidgets`` (thus not available in Qt Designer), you might want to build up you interface directly in code.
From this regard, there are no limitations in what you can do: just follow some good tutorial on how to deal with
``QMainWindow`` and Qt's layouts before jumping in.

In addition, you can still use ``accwidgets``' components by importing it (remember to add ``accwidgets``
in the core dependencies of your ``setup.py``). It's still recommended, where it makes sense, to isolate the
layouting code from the wiring (signal/slots) and from the rest of the application's logic.

Which means: **don't write your entire GUI as a single file**, unless is nothing more than a quick experiment.


.. index:: Resource Files (``.qrc``)
.. index:: ``.qrc`` files
.. _qrc_files:

Resource files (``.qrc``)
-------------------------
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




.. index:: Development Guidelines FAQ
.. _dev_guidelines_faq:

FAQ
===

*TODO*
