.. index:: Detailed Project Structure
.. _detailed_project_structure:

=======================
Explanation of the code
=======================

.. warning:: Work In progress

In this section we are going to describe in much higher detail what is the role of the most important files
in the template provided by ``bipy-gui-manager``, and the meaning of the code they include.

It is meant to help PyQt beginners find their way through the template.


.. toctree::

    81-detailed-project-structure

Prerequisites
=============
Before getting started, make sure you have a brand new project template created by ``bipy-gui-manager``
(see `here <1-bipy-gui-manager.html>`_). Let's assume it's called ``my-project``.
Also make sure you followed the instructions at the end of the installation process:

* Move into the project root directory (``my-project/``)
* Type ``source activate.sh``
* Open the project in PyCharm by typing ``pycharm.sh . &``

.. index:: setup.py (detailed explanation)
.. _setup.py-detailed:

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

.. index:: main.py (detailed explanation)
.. _main.py-detailed:

main.py: Start the application
==============================
The entry point specifies that the function to be called is the ``main()``, so let's have a look at what it does.

.. index:: main.py: Create the application (detailed explanation)
.. _main.py-app-creation-detailed:
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

would do nothing at all.

In order to have a window we have to instantiate a visible element, so either a
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

still doesn't work. ApplicationFrame *is* a graphical element, but one more step is missing which we're going to see
at the end of this file.

.. index:: main.py: GUI instantiation (detailed explanation)
.. _main.py-gui-instantiation-detailed:
Instantiate the actual GUI
--------------------------
The code proceed with these lines::

    # Instantiate your GUI (here the MainWidget class)
    main_widget = MainWidget(parent=window)

    # Add the main widget to the window
    window.setMainWidget(main_widget)

As the comment states, here we are generating the actual GUI. This implies that your GUI is defined into the
``MainWidget`` class, which we will cover right after this file.

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

.. index:: main.py: Window setup (detailed explanation)
.. _main.py-window-setup-detailed:
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

.. index:: main.py: Managing startup exceptions (detailed explanation)
.. _main.py-exceptions-detailed:
Manage an exception
-------------------
At the end of this block, there is an interesting ``except`` clause.
Quite a lot is going on in there, so let's read it line by line.

At first, ``window`` is replaced by a ``QWidget``::

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

.. index:: main.py: Launching the application (detailed explanation)
.. _main.py-launch-detailed:
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

.. index:: main.py: Summary (detailed explanation)
.. _main.py-summary-detailed:
Summary
-------
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
other cosmetic operations on the interface, which are less critical.

So make sure you understand well at least these four lines before proceeding.

.. index:: main_widget.py (detailed explanation)
.. _main_widget.py-detailed:
main_widget.py: Build your GUI's View
=====================================
As stated in the import statements in ``main.py``, the MainWidget class is defined into the ``main_widget.py`` file.
Let's have a look at its content.

.. index:: main_widget.py: Parent classes (detailed explanation)
.. _main_widget.py-parents-detailed:
Parent classes of a Qt View
---------------------------
To begin with, let's highlight the fact that MainWidget inherits from two classes::

    class MainWidget(QTabWidget, Ui_TabWidget):

`QTabWidget <https://doc.qt.io/qt-5/qtabwidget.html#details>`_ is a standard Qt widget for a tabbed container.
``Ui_TabWidget`` instead is imported from the ``generated/`` folder: this means that is the result of the compilation
of a ``.ui`` file.

.. note:: See `this section <https://acc-py.web.cern.ch/gitlab/bisw-python/pyqt-tutorial/docs/stable/2-project-structure.html#project-name-widgets-resources>`_
    to know more about how .ui files are automatically compiled into generated Python code
    every time the application is started.

A quick peek into ``widget/resources/generated/ui_main_widget.py`` clarifies that it is a plain Python object, with
no further parents::

    class Ui_TabWidget(object):

This helps greatly to prevent the
`diamond problem of multiple inheritance <https://en.wikipedia.org/wiki/Multiple_inheritance#The_diamond_problem>`_.

To summarize: **Ui_TabWidget is not a QObject**. It *contains* QObjects, but is not a QObject itself.
On the contrary, QTabWidget *is* a QObject subclass, and is the one that makes MainWidget a QObject as well.
This information can help you debug all those cases in which MainWidget might fail to instantiate.

Let's move on the the ``__init__()`` method.

.. index:: main_widget.py: View initialization (detailed explanation)
.. _main_widget.py-view-init-detailed:
Initializing a View
-------------------
Unsurprisingly, the first operation done in the constructor of MainWidget is to call the ``super`` method, passing
the ``parent`` parameter::

    def __init__(self, parent=None):
        super(MainWidget, self).__init__(parent)

This is necessary, as the ``parent`` parameter is needed by the parent QObject class to get deleted with
the window it belongs to. Failing to pass the ``parent`` to the superclass is equivalent to not setting it at all,
causing the same set of problems
`highlighted above <81-detailed-project-structure.html#main.py-gui-instantiation-detailed>`_ in the ``main()`` function.

After that, we see another very important call::

        # Setup itself as the view
        self.setupUi(self)

``setupUi()`` is one of the only two methods inherited by the generated class ``Ui_TabWidget``. Another quick peek
into its source code should clarify the purpose of this method: instantiating all the graphical elements, widgets,
layouts, etc... of the GUI, in order to replicate exactly the interface designed in Qt Designer.

After this call, the entire GUI is set up. All the object names defined in the .ui files are now available as attributes
of ``self`` and can be manipulated freely. However, heavy manipulation of such objects, especially to change their
default appearance, is discouraged: please use Qt Designer for this purpose.

So, if not for manipulation, why are the objects all available as attributes? You will see the reason in the next
paragraph.

.. index:: main_widget.py: Wiring the Model (detailed explanation)
.. _main_widget.py-model-detailed:
Instantiate and wire the Model
------------------------------
In Qt's ModelView paradigm, Views are usually responsible of instantiating their models and connect to them in the
constructor. In fact, the next line of the ``__init__()`` function is::

    # Instantiate the model
    self.model = SpinBoxModel()

We will have a better look at the content of ``SpinBoxModel`` later. However, we can already tell from the name that
it's a Model class.

Model classes are an interface between the Qt-based View objects and the backend system they need to interact with.
For example, when they receive a new value from the backend, they transform it into a Qt signal that can be understood
by, for example, a QLabel or a ListView.

In this case, the ``SpinBoxModel`` is the class that makes the QSpinBox able to set the value to the test device.
Let's see how this is actually done in the following lines.

First of all, we see one straightforward line of code that reads the Model and sets the initial value of the QSpinBox
(called ``self.frequency_spinbox``)::

    # Set the spinbox's initial value
    self.frequency_spinbox.setValue(self.model.get_frequency())

And then, the real connection::

    # Connect the spinbox to the control system
    self.frequency_spinbox.valueChanged.connect(self.model.set_frequency)

This syntax is part of `Qt Signals and Slots architecture <https://doc.qt.io/qt-5/signalsandslots.html>`_,
another cornerstone of the framework. Let's break it down.

The core element in this call is the ``.connect()`` method. ``.connect()`` is used to connect one Qt Signal to a
Qt Slot, as ``signal.connect(slot)``.

Signals can be imagined as sources of messages that are sent out from an object as a reaction to an event,
and might or might not carry extra information with them as a payload. For example, a lot of QWidgets expose the
``clicked()`` signal, which is emitted when they are clicked upon. Others expose the ``valueChanged(string)`` signal,
that carries with them the new value just set into them. And so on.

Slots can be imagined as observers of messages, and they trigger some action as a result of the reception of a message.
For example, many writeable QWidgets expose the slot ``clear()`` that empties their editable area. Others expose the
``setValue(string)`` slot, which will set a specific value into their editable area. The difference between slots and
regular function calls is that slots can be called by Qt itself when the right signal is received, and do not require a
direct call to be performed in the application code.

In addition, the signal's signature must match the slot's signature, i.e. if the signal carries one ``int``,
the slot must require only one single ``int`` as input.

This said, we can infer that ``valueChanged`` must be a signal, emitted when the QSpinBox content is edited, and that
``set_frequency`` is a slot, probably setting the value of the QSpinBox signal to the control system.

How can we verify this?

.. index:: main_widget.py: Find signals (detailed explanation)
.. _main_widget.py-signals-detailed:
Find signals
~~~~~~~~~~~~
To check if ``valueChanged`` is actually a signal with the expected signature, there are two strategies,
depending on the object the signal belongs to:

* If the object emitting the signal is a C++ Qt object, check its Qt documentation. Into each object's page there is
  a section dedicated to the signals it emits, but don't forget to check the signals emitted by their superclasses
  (like QWidget or QObject). A full lists of all the available members, including the ones from superclasses,
  is also available in the page.

* If the object emitting the signal is a PyQt QObject subclass, check into the source for the definition of this signal.
  In PyQt every QObject subclass can define new Signals in this way::

    from PyQt5.QtCore import QObject, pyqtSignal

    class MyPyQtObject(QObject):
        an_empty_signal = pyqtSignal()
        a_signal_with_a_value = pyqtSignal(float)


As you can see in both cases, signals can carry values of a specific type, in this case ``float``. Checkout
`PyQt's Documentation on the topic <https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html>`_ for
more details.

In this case, ``frequency_spinbox`` is a native QSpinBox Qt Widget, so we can see its signals in the Qt
`QSpinBox documentation <https://doc.qt.io/qt-5/qspinbox.html#signals>`_. As you can see, ``valueChanged`` is listed
and carries an ``int``, which according to the
`signal's documentation <https://doc.qt.io/qt-5/qspinbox.html#valueChanged>`_, represents the content of the
spinbox that was just set.

We will later see an example of a signal emitted by a PyQt object.

.. index:: main_widget.py: Find slots (detailed explanation)
.. _main_widget.py-slots-detailed:
Find slots
~~~~~~~~~~
To check if ``set_frequency`` is actually a slot with the expected signature, the procedure is very similar to the
signals one:

* If the object exposing the slot is a C++ Qt object, check its Qt documentation. Into each object's page there is
  a section dedicated to the slots it exposes, but don't forget to check the slots exposed by their superclasses
  (like QWidget or QObject). A full list of all the available members, including the ones from superclasses,
  is also available in the page.

* If the object exposing the slot is a PyQt QObject subclass, check into the source for the definition of this slot.
  In PyQt every QObject subclass can define new Slots in this way::

    from PyQt5.QtCore import QObject, pyqtSlot

    class MyPyQtObject(QObject):

        @pyqtSlot()
        def slot_with_no_parameters(self):
            pass

        @pyqtSlot(int)
        def slot_with_a_parameter(self, my_value: int):
            pass

As you can see in both cases, slots can receive values of a specific type, in this case ``int``. Note that the
decorator's declared types will make Python cast whatever value is received into that type, or throw an exception.
For example, if a slot requesting an ``int`` is connected to a signal emitting a ``float``, the mismatch might crash
the application or cause unexpected behavior.

Checkout
`PyQt's Documentation on the topic <https://www.riverbankcomputing.com/static/Docs/PyQt5/signals_slots.html>`_ for
more details.

In this case, ``get_frequency`` is a function exposed by SpinBoxModel, which is a PyQt QObject subclass and
therefore can define its own slots. In addition, we can see it defines a function which is decorated as ``pyqtSlot``
and has a signature that matches::

    @pyqtSlot(int)
    def set_frequency(self, value: int) -> None:
        ...

.. index:: main_widget.py: Summary of connect statememts (detailed explanation)
.. _main_widget.py-connect-summary-detailed:
Reviewing connect()
~~~~~~~~~~~~~~~~~~~
Once we verified that ``valueChanged`` is indeed a signal that matches the slot ``set_frequency``, let's see what the
``.connect()`` statement is there for.

The QSpinBox's ``valueChanged`` signal is emitted immediately after the value into the spinbox has changed: so,
as you type, is fired at each keystroke. ``valueChanged`` is emitted with an ``int`` value as a payload, and it goes
into the inner workings of Qt's Meta-Object System to be dispatched to all listeners.
Here, Qt figures out whether anyone is listening to this signal and finds that the ``set_frequency`` slot is connected.
So it calls the slot, passing the payload ``int`` as a parameter.

This all happens in an asynchronous matter. For more details on the Qt Meta-Object System, check out the
`C++ documentation <https://doc.qt.io/qt-5/metaobjects.html>`_ and its
`support in PyQt <https://www.riverbankcomputing.com/static/Docs/PyQt5/metaobjects.html>`_.

.. note:: The following method call sets up the plot in the main window. Setting up the plot is in principle
    the same as for the QSpinBox: loading initial values and the calling ``.connect()`` a few times. However,
    we will now skip over this part and revisit it in a later paragraph.

.. index:: models.py (detailed explanation)
.. _models.py-detailed:
models.py: Interface to the control system
==========================================
Let's finally have a better look at the Model itself now.

Models are located in ``my-project/my_project/models/models.py``, which as we can see contains three classes:
SpinBoxModel, DeviceTimingSource and SinglePointSource. The last two are related to the plotting, which we will
cover better in a dedicated section, while you should already be somewhat familiar with SpinBoxModel.

.. note:: Please ignore the large comment in the import statements for now.
    Or, if you are interested, head to the `papc section <89-papc.html>`_ to learn more.

First of all, let's note again that SpinBoxModel inherits from QObject::

    class SpinBoxModel(QObject):
        ...

This is necessary for an object to be able to expose slots or emit signals. Forgetting this import will make
the code break as soon as the first ``.connect()`` tries to address a "slot" from this class.

Let's move on to the ``__init__()``::

    def __init__(self):
        super(QObject, self).__init__()
        # Create the PyJAPC connector
        self.japc = pyjapc.PyJapc()
        # Use the empty selector
        self.japc.setSelector("")

This few lines of code should come to no surprise to most readers. In short, ``super()`` is called to initialize
QObject. Then, a ``PyJapc`` instance is created and, in the following line, the empty selector is given to it.

The content of this method is supposed to initialize the connection to the control system, in this case to PyJAPC.
Such initialization has nothing that is Qt-specific and you should refer to your library's documentation to
understand better how to initialize the connection.

The rest of the class contains two methods. The first is ``get_frequency()``, which you might remember we already
met in MainWidget's initialization::

    def get_frequency(self) -> float:
        return self.japc.getParam("BISWRef1/Settings#frequency")

As you can see, it is nothing more than a simple getter that translates the PyJAPC GET operation into a more
system-agnostic call. Note that this function is not a Qt entity in any way: is simply a Python method.

The situation is slightly different for the second method, ``set_frequency()``::

    @pyqtSlot(int)
    def set_frequency(self, value: int) -> None:
        self.japc.setParam("BISWRef1/Settings#frequency", value)

The method itself is also nothing more than a setter, wrapping the PyJAPC specific syntax into an agnostic one.
However, this method is a PyQt Slot as well: this means that can be used in a ``connect()`` statement and is
run automatically as soon as its matching signals are emitted.

.. index:: Plots with accwidgets (detailed explanation)
.. _plotting-detailed:
Plots with accwidgets
=====================
