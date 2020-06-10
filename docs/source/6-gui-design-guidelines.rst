.. index:: GUI Design Strategies
.. _gui_design:

=====================
GUI Design Guidelines
=====================

PyQt5 allows for two strategies for designing GUIs: either with the Qt Designer, which generates XML ``.ui`` files,
or through code, in ``.py`` files.

In general, for complex applications, it is recommended to design the interface with
`Qt Designer <https://doc.qt.io/qt-5/qtdesigner-manual.html>`_.
However, in special cases it might be more convenient to use only code: in the end it's up to you to decide what
is the more sensible approach for your specific case.

If in doubt, use the Qt Designer.


.. index:: Qt Designer files
.. index:: .ui files
.. _ui_files:

Design with Qt Designer (using ``.ui`` files)
=============================================
The Qt Designer version shipped with Acc-Py is basically identical to any vanilla Qt Designer, so any good
`tutorial <https://relentlesscoding.com/2017/08/25/tutorial-rapid-gui-development-with-qt-designer-and-pyqt/#installation>`_
on the Internet should be good to help you get started.

Once you finished your design, you will end up with one or more XML ``.ui`` files.
These files cannot be loaded directly in a PyQt application (unlike QML files), but have to be compiled.

.. warning:: QML files are **not recommended** and **not supported** by Acc-Py's team or by BI, due to its
    remarkably poor plotting performance and their need for JavaScript.

The compilation can be done automatically, but also manually. if you are using the boilerplate code from
``bipy-gui-manager``, the automatic compilation is already setup for you. If you want to know the details of how
it works, or you need to compile manually for any reason, check `this page <90-advanced-xml.html>`_.


.. index:: Using ``.ui`` files
.. index:: ``.ui`` files usage
.. _ui_files_usage:

Using the ``.ui`` files in code
===============================
Once you created your interface, you can load it into your application.

The loading is done into the Presenter, that is, into any file in the ``widgets`` folder::

    import sys
    from PyQt5 import QtCore, QtGui, QtWidgets
    from PyQt5.QtWidgets import QApplication
    from my_app.generated.main_window import Ui_Form

    class MainWidget(QtWidgets.QMainWindow, Ui_Form):
        def __init__(self, parent=None):
            super(MainWidget, self).__init__(parent)
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
    PyQt4-style, but works just fine. Naturally, all your widgets will be namespaced under ``self.ui``
    instead of being directly accessible under ``self``.


.. index:: Design GUI in code
.. _gui_py_files:

Design in code
==============
If you have very specific use cases, or your application is made mostly of reusable widgets that don't come from
``accwidgets`` (thus not available in Qt Designer), you might want to build up you interface directly in code.
From this regard, there are no limitations in what you can do: just follow some good tutorial on how to deal with
``QMainWindow`` and Qt's layouts before jumping in. In this case, however, we recommend caution, as GUIs developed
in code are inherently harder to maintain.

While building a GUI in code you can still use ``accwidgets``' components by importing them
(remember to add ``accwidgets`` in the core dependencies of your ``setup.py``).
It's still recommended, where it makes sense, to isolate the layouting code from the wiring (signal/slots)
and from the rest of the application's logic.

Which means: **don't write your entire GUI as a single file**, unless is nothing more than a quick experiment.


.. index:: Resource Files (``.qrc``)
.. index:: ``.qrc`` files
.. index:: Loading images with Qt Designer
.. _qrc_files:

Resource files (``.qrc``)
=========================
If you're adding static resources to your interface (like images) you have to use a **resource file (.qrc)**.

If you are using Qt Designer, the procedure goes as follow:

 * Add a Label to your GUI or select an existing one.

    .. raw:: html

             <img src="../_static/qrc_files/step-1.png" />

 * In the Property Editor, go to the ``pixmap`` property and click on the ``...`` button.

    .. raw:: html

             <img src="../_static/qrc_files/step-2.png" />


 * Clicking on the wrench icon on the ``Select Resource`` dialog that opens up.

    .. raw:: html

             <img src="../_static/qrc_files/step-3.png" />


 * This will open a new ``Edit Resources`` dialog. Use the buttons on the bottom left corner to create a new
   file in the folder of your resources, named for example ``images.qrc``.

    .. raw:: html

             <img src="../_static/qrc_files/step-4.png" />


 * In the same dialog, use the first button in the bottom center to add a prefix (a namespace) for your images,
   for example ``images``.

    .. raw:: html

             <img src="../_static/qrc_files/step-5.png" />


 * In the same dialog, use the second button in the bottom center to add a file under the selected prefix.

    .. raw:: html

             <img src="../_static/qrc_files/step-6.png" />


 * Save your changes.

    .. raw:: html

             <img src="../_static/qrc_files/step-7.png" />


 * Back to the ``Select Resource`` dialog you will now be able to select your image.
   Select it and confirm.

    .. raw:: html

             <img src="../_static/qrc_files/step-8.png" />

 * The label should now contain your image. If you want the image to fit the label size, select the ``scaledContent``
   property just below ``pixmap``. Save your ``.ui`` file.

    .. raw:: html

             <img src="../_static/qrc_files/step-9.png" />

 * If your Designer files are compiled automatically, your ``.qrc`` file will be automatically detected and compiled
   as soon as you start your application. If not, check out `the advanced topics page <90-advanced-xml.html>`_
   to know more about how to compile these files manually.

 * You can now launch the application and make sure it runs. After the first run,
   you should see a file called ``images_rc.py`` among your generated ``ui_*.py`` files.

    .. raw:: html

             <img src="../_static/qrc_files/step-10.png" />



.. index:: Development Guidelines FAQ
.. _dev_guidelines_faq:

FAQ
===

*TODO*
