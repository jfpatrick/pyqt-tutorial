.. index:: Detailed Project Structure
.. _detailed_project_structure

=======================
Explanation of the code
=======================

.. warning:: Work In progress

In this section we are going to describe in much higher detail what is the role of the most important files
in the template provided by ``bipy-gui-manager``, and the meaning of the code they include.

It is meant to help PyQt beginners find their way through the template.


.. toctree::

    self

Prerequisites
=============
Before getting started, make sure you have a brand new project template created by ``bipy-gui-manager``
(see `here <1-bipy-gui-manager.html>`_). Let's assume it's called ``my-project``.
Also make sure you followed the instructions at the end of the installation process:

* Move into the project root directory (``my-project/``)
* Type ``source activate.sh``
* Open the project in PyCharm by typing ``pycharm.sh . &``


setup.py: Find the entry point of an app
========================================
One important point to keep in mind, once you start a new project or checkout an existing one, is how to find or create
the entry points (check out this `page <2-project-structure.html#entry-points>`_ to know more about what entry
points are).

They are defined in the ``setup.py`` file, so let's open it. Near the end, there should be an entry similar to the
following::

    entry_points={
        'console_scripts': [
            # MODIFY: remove this line and add a pointer to the startup function of your app.
            # This means: 'my-project' launches "my_project/main.py:main()"
            'my-project=my_project.main:main',
        ],
    },

Indeed, typing ``my-project`` in your shell would start executing from the ``main()`` function of the
``main.py`` file of the ``my_project`` module (note the module name is the module name, not really ``my_project``).

There might be multiple entry points to start CLI clients or windows with different setups. In the template, though,
there is one single entry point, which points to the ``main.py`` file.

Let's have a look at what it contains.

main.py: Open the window
========================
The entry point specifies that the function to be called is the ``main()``, so let's have a look at what it does.

Create the application
----------------------
In the first two lines, we see the code instantiates a ``QApplication`` and an ``ApplicationFrame``::

    # Instantiate the QApplication
    app = QApplication(sys.argv)

    # Instantiate the ApplicationFrame
    window = ApplicationFrame()

A ``QApplication`` object literally represents an "empty" Qt Application, without any window. For example, a code
like the following::

    def main():
        app = QApplication()
        return

would do nothing at all. In order to have a window we have to instantiate a visible element, so either a
`QWidget <https://doc.qt.io/qt-5/qwidget.html#details>`_, or a
`QMainWindow <https://doc.qt.io/qt-5/qmainwindow.html#details>`_, etc.
In this case, we are instantiating an `ApplicationFrame <https://gitlab.cern.ch/bisw-python/be-bi-application-frame>`_
object, which is a CERN widget that subclasses ``QMainWindow``. It is little more than a frame that includes a
few standard widgets around the edges of the window, like the logs console, the RBAC button, etc. Check its
documentation to learn more about it.

There is no need to explicitly connect the two objects: the ApplicationFrame automatically belongs to the QApplication
instance. This fact brings a corollary: do not try to instantiate multiple ``QApplication`` objects in the same method,
as it will cause trouble and is almost surely unnecessary.

However, note that code like this::

    def main():
        app = QApplication()
        window = ApplicationFrame()
        return

will still not work. ApplicationFrame is a graphical element, but one more step is missing which we're going to see
at the end of this file.

Instantiate the actual GUI
--------------------------
The following lines are::

    # Instantiate your GUI (here the MainWidget class)
    main_widget = MainWidget(parent=window)

    # Add the main widget to the window
    window.setMainWidget(main_widget)

As the comment states, this line is finally generating your GUI. This implies that your GUI is defined into the
``MainWidget`` class, which we will cover in a moment.

In the second line, ``setMainWidget()`` is a method exposed by ApplicationFrame to load the GUI into its central area.

For now, let's just note how ``main_widget`` requires a ``parent`` parameter to be set to ``window``, which was the
ApplicationFrame object. This is very important for garbage collection and to avoid memory leaks, because it tells
Qt that, when ApplicationFrame is deleted (fro example, the app exits or the window is closed), also all its
children, including ``main_widget``, should be deleted.

Failing to set the parent to widgets in general does not cause immediately visible problems. You can try for yourself:
if you remove ``parent=window`` from the constructor call, the application will most likely start without an issue
and will also look just right.
However, it is very fragile and can cause very obscure ``SEGFAULT``s and core dumps as soon as some multithreading
gets in the way, which in Qt happens almost in every application. To be safe, is always recommended to set the
parent meaningfully.

Setup the window
----------------
After instantiating the GUI, the code proceeds to set a few window parameters.

The first one sets the window icon::

    # Apply small customizations to the application (window title, window icon...)
    icon_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'widgets/resources/images/CERN_logo.png')
    window.setWindowIcon(QIcon(icon_path))

Note how you have to set the path to the icon. Unfortunately, in Python relative paths are not resolved starting
from the position of the file which is being executed, but from the current working directory, which can be anywhere
on the filesystem. For as ugly as it looks, ``os.path.dirname(os.path.realpath(__file__))`` is the way to get the
path to the file which is currently running, and then to resolve the icon path correctly.

Note how you don't necessarily need a Resource File (see
`here <2-project-structure.html#project-name-widgets-resources>`_ for info) to load the icon.

The second line sets the window size in pixels::

    # Set the initial size of the window
    window.resize(800, 600)

And the last sets the window title, using the content of the ``APPLICATION_NAME`` constant::

    # Set the window title
    window.setWindowTitle(APPLICATION_NAME)

Manage an exception
-------------------
At the end of this block, there is an interesting ``except`` clause.
Quite a lot is going on in there, so let's read it line by line.

At first, ``window`` is replaced by a ``QWidget``:

        window = QWidget()

in fact the exception might have been thrown during the instantiation of ApplicationFrame,
so we have to replace it with a fallback object like QWidget, which is extremely unlikely to fail.

After the base window is created, we create a `QMessageBox <https://doc.qt.io/qt-5/qmessagebox.html#details>`_ object::

    dialog = QMessageBox(parent=window)

This is going to be an error dialog which we use to show the exception that prevented the application from starting up.

This all happens in the following line, where we set the
`critical() <https://doc.qt.io/qt-5/qmessagebox.html#critical>`_ method with some text explaining the situation::

    dialog.critical(window,
                    "Error",
                    "An Exception occurred at startup:\n\n{}\n\n".format(e) +
                    "See the logs for more information, " +
                    "and please report this issue to {} ({})".format(AUTHOR, EMAIL))

The arguments are, in order, the parent, the title, and the text of the dialog.

The ``critical`` method makes sure the dialog has the right icon and behaves according to your system configurations on
critical alerts, and has more parameters, like which buttons to display, which is the default response, etc...

.. note:: Note one fundamental point: calling ``critical`` will start its own event loop and immediately
    display  the message box. This event loop is minimal and private to the message box, and differs substantially from
    the main event loop that we're going to start at the end of the ``main()`` method.

Eventually, we call `window.deleteLater() <https://doc.qt.io/qt-5/qobject.html#deleteLater>`_::

        window.deleteLater()
        return

This method tells Qt that, as soon as it gets control back from the application, it should delete the specified object.
In this case, this thread gains back control once the user closes the dialog (because it exits the dialog's event loop),
and it immediately proceeds to destroy the ``window`` object.

As an automatic consequence of closing the last (only) window existing in the QApplication object (``app``),
Qt gracefully closes the entire application and returns.

Note that this delete operation is performed in a separate thread in the majority of cases, but not always,
so pay attention to it.

.. note:: You can test this behavior by adding a ``raise ValueError("Hello!")`` in the body of the ``try`` statement.

Start the application
---------------------
Now that everything is ready to go, we can finally launch the application::

    # Enter the event loop by showing the window
    window.show()

This line tells Qt to enter the event loop by showing the ``window`` object to the users. This call is blocking and
from this line on, nothing will be executed until the window is closed.

.. note:: You can try it yourself by putting a ``print`` statement after this line.

In fact, the following line is little more than a hack to help Qt quit gracefully::

    # Once left the event loop, terminates the application
    sys.exit(app.exec_())

This is unfortunately necessary in PyQt, as applications that entered the event loop but forgot to terminate explicitly
might just stay around as zombies indefinitely. Note that in the case of the dialog we didn't need this hack, because
the application never entered the main event loop, but used its own.

Recap
-----
The essence of the ``main.py`` file could be packed in these three lines of code::

    def main():
        app = QApplication(sys.argv)
        window = QWidget()
        window.show()

If you try this, you will get an empty window as a result. By adding one line::

    def main():
        app = QApplication(sys.argv)
        window = QWidget()
        main_widget = MainWidget(parent=window)
        window.show()

you will get your GUI displayed in the above mentioned window. All the rest of the code does either error recovery or
other cosmetic operations on the interface, which are way less critical.

So make sure you understand well at least these four lines before proceeding.


