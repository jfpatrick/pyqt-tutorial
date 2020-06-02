.. index:: Development Tools
.. _tools

=================
Development Tools
=================

.. index:: PyCharm
.. _pycharm

PyCharm
=======

The Acc-Py team offers also a shared PyCharm instance to ease the development on TN machines.
Such instance is located under::

	/acc/local/share/python/pycharm/pycharm-community-2019.2.3/

and can be launched by executing::

    /acc/local/share/python/pycharm/pycharm-community-2019.2.3/bin/pycharm.sh

If you have any other PyCharm installation on your ``PATH`` already, you can also simply type::

	charm

to launch it.

Remember that adding a path to a folder after the command makes PyCharm load that folder as a starting project.

.. warning::
    At the time of writing (May 2020) PyCharm 2019 presents one serious bug with the Open Project folder explorer,
    which makes it hang for several minutes every time it tries to access an AFS directory (like most user's homes).
    Therefore it's important to avoid using it by launching PyCharm from the relevant directory directly.

.. index:: Qt Designer
.. index:: designer
.. _qtdesigner

Qt Designer
===========

The recommended way to implement your PyQt5 GUIs is to use ``.ui`` files to define your interface. Therefore,
Acc-Py-PyQt provides you with a shared instance of the **Qt Designer**.

You can launch it by typing::

	designer <path-to-your-file.ui>

Some CERN libraries like ``accwidgets`` (see next section) provide extra widgets that can be used from the Designer.
However, those widgets are not picked up automatically: you should make sure you have the ``PYQTDESIGNERPATH``
environment variable set to the correct folder. For example, for ``accwidgets`` the value would be::

    PYQTDESIGNERPATH=<path-to-your-project-virtualenv>/lib/python3.6/site-packages/accwidgets/graph/designer

Refer to your library's documentation to know which paths to add to this variable to enable their widgets.

.. note:: If you have trouble with a library, you can check the
    `official Qt documentation <https://doc.qt.io/qtcreator/adding-plugins.html#locating-qt-designer-plugins>`_
    for hints.

.. index:: Development Tools FAQ
.. tools_faq

FAQ
===

*TODO*
