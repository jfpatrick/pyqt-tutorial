.. index:: Development Tools
.. _tools:

=================
Development Tools
=================

In this section we cover the most relevant development tools for PyQt Expert GUIs: **PyCharm** and **Qt Designer**.
In addition we also describe briefly how to create a Continuous Integration pipeline with **GitLab CI**.

.. index:: PyCharm
.. _pycharm:

PyCharm
=======

PyCharm is the recommended IDE for developing Python applications. If you're new to it, you can find some tutorials
`below <3-tools.html#pycharm_tutorials>`_.

The Acc-Py team offers also a shared PyCharm instance on TN machines. If you are using the template provided by
``bipy-gui-manager``, it is already on your ``PATH`` and it can be launched with::

    pycharm.sh . &

from your project's root directory (the folder that contains your ``setup.py``).

Otherwise, you can find the instance under::

	/acc/local/share/python/pycharm/pycharm-community-2019.2.3/

and can be launched by executing::

    /acc/local/share/python/pycharm/pycharm-community-2019.2.3/bin/pycharm.sh . &

always from your project's root directory.

Remember that adding a path after the command makes PyCharm load that folder as a starting project. So if you're
launching PyCharm from a different folder, replace the dot with the path to the project's root folder.

.. note::
    In some cases PyCharm might not manage to find your virtual environment and will throw a lot of exceptions
    regarding broken imports and features unsupported in Python 2.7.
    If this happens to you, apply this extra setup step explained on the
    `Acc-Py Wikis <https://wikis.cern.ch/display/ACCPY/PyQt+distribution#PyQtdistribution-LaunchingPyCharmfromthesystemmenu>`_

.. warning::
    Technically PyCharm does not strictly need a path to start. For example, desktop application launchers do not
    provide a path to it.

    However, at the time of writing (May 2020) PyCharm presents one serious bug with the Open Project folder explorer,
    which makes it hang for several minutes every time it tries to access an AFS directory (like most user's homes).
    Therefore it's important to launch PyCharm from the relevant directory, as explained above, until the issue is
    fixed.

.. note:: Although recommended, PyCharm is not mandatory. If you're comfortable with other editors (VSCode,
    Eclipse, Emacs, ...) feel free to use them instead.


.. index:: PyCharm Tutorials
.. _pycharm_tutorials:

PyCharm Tutorials
-----------------

Please email the maintainers of this tutorial with any other good PyCharm tutorial you find on the Web, and it will be
added to the list.

Video tutorials
~~~~~~~~~~~~~~~

 * Official JetBrains tour of PyCharm features: https://www.youtube.com/playlist?list=PLQ176FUIyIUZ1mwB-uImQE-gmkwzjNLjP

Web Pages
~~~~~~~~~

 * Official JetBrains Getting Started page: https://www.jetbrains.com/help/pycharm/quick-start-guide.html


.. index:: Qt Designer
.. index:: designer
.. _qtdesigner:

Qt Designer
===========

The recommended way to implement your PyQt5 GUIs is to use ``.ui`` files to define your interface. Therefore,
Acc-Py-PyQt provides you with a shared instance of the **Qt Designer**.

Once you activated the virtuanenv, you can launch it by typing::

	designer <path-to-your-file.ui>

Some CERN libraries like ``accwidgets`` (see `next section <5-libraries.html#accwidgets>`_) provide extra widgets
that can be used from the Designer.
However, those widgets are not picked up automatically: you should make sure you have the ``PYQTDESIGNERPATH``
environment variable set to the correct folder. For example, for ``accwidgets`` the value would be::

    PYQTDESIGNERPATH=<path-to-your-project-virtualenv>/lib/python3.6/site-packages/accwidgets/graph/designer

Refer to your library's documentation to know which paths to add to this variable to enable their
Qt Designer widgets plugin. If you have trouble with a library, you can also check the
`official Qt documentation <https://doc.qt.io/qtcreator/adding-plugins.html#locating-qt-designer-plugins>`_
for hints.

.. note:: You can also build your own custom Qt Designer plugins! See the relevant page on the
    `Acc-Py wikis <https://wikis.cern.ch/display/ACCPY/Widgets#Widgets-ImplementingcustomQtWidgets>`_
    for an overview of the process.


.. index:: Qt Designer Tutorials
.. _qtdesigner_tutorials

Qt Designer Tutorials
---------------------

Video Tutorials
~~~~~~~~~~~~~~~

 * Tech With Tim's video on Qt Designer: https://www.youtube.com/watch?v=FVpho_UiDAY
   Part of a larger collection of videos on PyQt in general.

 * Guyon Morée videos on Qt Designer: although made with PyQt4, the Qt Designer related part is still valuable.

    - Part 1 https://www.youtube.com/watch?v=LYF0spYkXUs
    - Part 2 https://www.youtube.com/watch?v=JOuCuLHmk3o

Web Pages
~~~~~~~~~

 * Official Qt Guide to Qt Designer: https://doc.qt.io/qt-5/qtdesigner-manual.html

 * Relentless Coding's blog post about Qt Designer:
   https://relentlesscoding.com/2017/08/25/tutorial-rapid-gui-development-with-qt-designer-and-pyqt/#our-goal



.. index:: Continuous Integration
.. index:: GitLab CI
.. _gitlab_ci:

GitLab CI
=========

GitLab CI is a powerful tool to ensure the code you publish on GitLab works as expected.
It's a pipeline that runs a number of operations on your code, namely running tests in an isolated container,
do linting, producing coverage reports, and many more.

It is mostly setup already by the Acc-Py team, and some extra customizations are added by ``bipy-gui-manager``.
To learn more about the nature of such modifications, check out the ``.gitlab-ci.yml`` file description
`in the relevant page <2-project-structure.html#gitlab-ci-yml>`_. See also the
`testing section <7-testing.html#testing>`_ for troubleshooting tests that run locally but fail on GitLab.

Tips and Tricks
---------------

.. index:: Add coverage badge to your repo
.. _add_coverage_badge:

Add coverage badge
~~~~~~~~~~~~~~~~~~~
In GitLab's side bar, press ``Settings > General > Badges``. The fill the fields as follows::

    Name: coverage
    Link: https://gitlab.cern.ch/<user or group>/<my-project>/pipelines
    Badge image URL: https://gitlab.cern.ch/<user or group>/<my-project>/badges/master/coverage.svg

The next time a pipeline runs on master, the number should be updated.


.. index:: Make screenshots during the tests
.. _test_screenshots:

Make screenshot during the tests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
*TODO Check Acc-Py documentation*




.. index:: Development Tools FAQ
.. _tools_faq:

FAQ
===

*TODO*
