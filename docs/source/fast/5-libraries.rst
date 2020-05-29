.. index:: Libraries
.. _libraries

Libraries
----------

.. index:: GUI Libraries
.. _gui_libraries

GUI Libraries
^^^^^^^^^^^^^

The Acc-Py team provides and maintain a lot of Python libraries. Here is a non-exhaustive list of the most
important ones related to PyQt5 (May 2020):

.. index:: ComRAD
.. _comrad

ComRAD
~~~~~~~

ComRAD is CO's Rapid Application Development Framework for PyQt5 GUIs. It can be used to create GUIs by solely
using Qt Designer. In most cases users are able to develop fairly complex interfaces without the need to write
any Python code.

ComRAD is the perfect tool for quick prototypes and for getting familiar with the Qt Designer and basic Qt principles
before diving into the code. If you are a beginner in Python or never worked with Qt before, you can use it as
a starting point.

Please refer to the
`ComRAD documentation <https://acc-py.web.cern.ch/gitlab/acc-co/accsoft/gui/rad/accsoft-gui-rad-comrad/docs/stable/>`_
to learn more about this tool.

.. note:: ComRAD also includes a set of reusable widgets that are accessible from its own Qt Designer instance.
    Such widgets are currently ComRAD specific, but they will eventually be merged with accwidgets, to ease the
    transition effort from one tool to the other.
    ** PLEASE UPDATE THIS SECTION **

.. index:: accwidgets
.. _accwidgets

accwidgets
~~~~~~~~~~

`accwidgets` is a collection of widgets for PyQt5 for the Acc-Py community. It includes components like:

 - **LED widgets** to indicate status
 - **Property Editor widgets**, that shows the fields of a device/property (similar to the Knob of a WorkingSet)
 - **Plotting widgets** built upon an `extended <https://gitlab.cern.ch/fsorn/pyqtgraph-extensions>`_ version of
   `PyQtGraph <https://gitlab.cern.ch/acc-co/accsoft/gui/accsoft-gui-pyqtgraph>`_.

The plotting widgets make for an extensive share of accwidgets itself, and are commonly referred as the `accgraph`
module.

Many more widgets are likely to be added to this package in the future, so always refer to the
`official documentation <https://acc-py.web.cern.ch/gitlab/acc-co/accsoft/gui/accsoft-gui-pyqt-widgets/docs/stable/>`_.


.. index:: Control System Libraries
.. _control_system_libraries

Control System Libraries
^^^^^^^^^^^^^^^^^^^^^^^^

In addition to the GUI Libraries, the Acc-Py team also maintains most of the libraries that access the control
system (RDA, JAPC, LSA, ... ). Here is a non-exhaustive list of the most relevant ones:

    - PyJAPC: Python binding for JAPC. See the
        `documentation <https://acc-py.web.cern.ch/gitlab/scripting-tools/pyjapc/docs/stable/>`_.
    - PyRDA: Python binding for RDA. See the `documentation [missing link]`.
    - PyLSA: Python binding for LSA. See the `documentation [missing link]`.
    - papc: pure Python JAPC devices simulator. Useful for tests and simulations. See the
        `documentation <https://acc-py.web.cern.ch/gitlab/pelson/papc/docs/stable/>`_.
    - accjapc: PyQt friendly interface to JAPC devices, supports signals and slots internally. See the
        `documentation <https://acc-py.web.cern.ch/gitlab/isinkare/accjapc/docs/stable>`_.
    - etc...