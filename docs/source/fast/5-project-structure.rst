.. index:: Project Structure
.. _project_structure

Project Structure
-----------------

All BI Expert GUIs should try to use a common project structure. This is also the default
structure of projects created with ``bipy-gui-manager``.

You can find the project template in
`this GitLab repo <https://gitlab.cern.ch/bisw-python/be-bi-pyqt-template>`_.

The template provides:

 - A sane folder structure for your code, based on the **MVP architecture**,
 - A test setup ready for unit tests and GUI tests (based on ``pytest-qt``),
 - A minimal simulation environment for your tests (based on ``papc``),
   that can be extended to simulate your real data sources (FESA, NXCALS, ...)
 - A ``setup.py`` to customize for quick packaging & release, with entry points,
 - A ``.gitignore`` for Python artifacts,
 - A ``.gitlab-ci.yml`` supporting GUI testing out of the box and coverage reports,
 - A small ``activate.sh`` activation script to activate both your virtualenv and Acc-Py,
   and sets up some env vars for Qt Designer.

We are going to cover each of these files one by one.

.. index:: .gitignore
.. _gitignore

.gitignore
^^^^^^^^^^^
Typical ``.gitignore`` file that excludes most Python artifacts. You can add your
own files/folders to exclude them from version control.

If you have doubts about this file, check
`this link <https://www.freecodecamp.org/news/gitignore-what-is-it-and-how-to-add-to-repo/>`_ or Google it.

.. index:: .gitlab-ci.yml
.. _gitlab-ci_conf

.gitlab-ci.yml
^^^^^^^^^^^^^^^
This file configures GitLab CI to run your tests each time you push your code
to the repository.
It differs a lot from the default obtained by executing ``acc-py init-ci``, because it has been configured to:

 - Run headless GUI tests with ``pytest-qt``
 - Provide a coverage report that you can use as a repository badge.
 - Do not deploy automatically on the CERN Python repository.

You can  modify it to add more tasks, deploy automatically, do linting, or anything else. For more information, check
`Acc-Py documentation <https://wikis.cern.ch/display/ACCPY/GUI+Testing>`_ or Google the file name.

.. index:: activate.sh
.. _activate.sh

activate.sh
^^^^^^^^^^^

Small bash script sourcing, in order, Acc-Py-PyQt and your virtualenv (assuming it's called venv and lives in the
current directory). This ensures that the overall environment is setup correctly.

It also sets the ``PYQTDESIGNERPATH`` in case you want to use Qt Designer with the ``accwidget``'s
plugin. See the Libraries sections (under :ref:`accwidgets`) for a recap on this specific env var.

.. index:: README.md
.. _readme

README.md
^^^^^^^^^^
A simple Markdown based README file. It's recommended to add some information to it, including at the minimum what
your project is, how to run it, who's the author/maintainer and any precautions to take when running/debugging
(i.e. is this GUI operational?)

.. note:: ``bipy-gui-manager`` will create for you a standard ``README.md`` with some basic information.
    You're still encouraged to expand it with a meaningful description of your project's
    goals and features.

.. index:: setup.py
.. _setup.py

setup.py
^^^^^^^^
This file defines your application as a Python package. You can learn more about Python packaging in
`here <https://packaging.python.org/>`_.

It gathers a few important information, namely:

    - A list of all your **project's dependencies**, grouped by usage (core, testing, development, documentation, etc.),
    - The package's **name**, **description** and **version**,
    - The code's **author** and their contact information,
    - Eventual **entry points** of your application,
    - Python version's compatibility,
    - and more.

.. note:: ``bipy-gui-manager`` partially populates this file with proper values, but you're always free to modify it.
    Notably, it creates an entry point called ``<project_name>`` (replace with the actual project name!) that can be
    used to launch your application directly, without invoking explicitly the Python interpreter.

.. index:: project_name/
.. _project_folder

<project_name>/
^^^^^^^^^^^^^^^
This is where your project's code lives. All the files included in this folder will be packaged and distributed
with your code. When importing from the various scripts, this folder's name is the root of all the imports.

.. note:: While top-level project names are recommended to use dashes as separators, modules must use underscores to
    comply with Python syntax. Therefore, if your project was called ``my-test-project``, this folder will be called
    ``my_test_project``.

.. index:: main.py
.. _main.py

<project_name>/main.py
^^^^^^^^^^^^^^^^^^^^^^
The application's entry point. You can edit the ``main()`` function to load your GUI, as specified in the comments in the
file itself, but this file should contain no more than the small function that starts the event loop (and at most do
some error handling). The rest of the logic will go in the other folders.

In the demo application, ``ExampleWidget`` (from ``<project_name>/widgets/example_widget.py``) is instantiated and 
loaded here.

.. index:: widgets/
.. _widgets_folder

<project_name>/widgets/
^^^^^^^^^^^^^^^^^^^^^^^
This contains the components of your application. In an MVP model, these are the Presenters: they instantiate the Views 
(see ``<project_name>/resources``) and wire them to the Models (see ``<project_name>/models``), acting as an 
intermediary when required.

In the demo application, ``ExampleWidget`` is the Presenter and lives in there, in ``example_widget.py``.

.. index:: resources/
.. _resources_folder

<project_name>/resources/
^^^^^^^^^^^^^^^^^^^^^^^^^
This folder contains multiple entities, all related to the static GUI's
structure definition. These represent the View from an MVP perspective.
They are:

 - **.ui files**. These are generated by Qt Designer and are XML files describing your GUI's layout, with no logic.
 - The ``images/`` folder containing static resources (PNG, GIF, etc...) and **.qrc files**. These files are
    Qt's Resource Files and are used to load static files, like images and icons, into the GUI.
 - The ``generated`` subfolder, that contains generated code of two kinds:

     - **ui_<view_name>.py files**. These files are generated by ``pyuic5`` basing on the *.ui file with matching name.
        NEVER MODIFY THESE FILES: they contain generated code and every modification will be erased at the next run
        of ``pyuic5``.

     - **<folder_name>_rc.py files**. These are generated by ``pyrcc5`` basing on the *.qrc files with a matching name.
        NEVER MODIFY THESE FILES: they contain generated code and every modification will be erased at the next run
        of ``pyrcc5``.

    .. note:: More instruction on how to use ``pyuic5`` and ``pyrcc5`` (or a way to go around them) coming soon.

    In this folder, you should modify the ``*.ui`` and ``*.qrc`` files only with QtDesigner (unless you really know what
    you're doing) and load the Views into the Presenters (``widgets/`` folder) by importing the ``ui_*.py`` files from
    the generated folder. You can see this happening in the ``ExampleWidget`` class.

.. index:: models/
.. _models>folder

<project_name>/models/
^^^^^^^^^^^^^^^^^^^^^^
This folder contains the Models of your application. The Model manages any object connecting to the control system,
like PyJAPC instances, NXCALS connections, etc. Models should send their data to the Views by emitting *signals* that
match corresponding *slots* in the View or Presenter.

In the demo application, this folder contains a ``data_sources.py`` file that hosts all the Model classes.
You are encouraged to create as many files as you wish. In this file, the ``ExampleModel`` class does mostly PyJapc SET
operations, while the plots' models retrieve data. No direct operation on the GUI is done here.

.. index:: papc_setup/
.. _papc_setup

<project_name>/models/papc_setup/
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
This folder contains a barebone ``papc`` setup to sandbox your application. ``papc`` is a library that can trick your
application into believing it's connecting to the control system, while it's receiving simulated data instead.
This also allows control system apps to run in a sandbox also on non-TN machines, without the need of any modification.

``papc`` is primarily an option for creating meaningful and thorough GUI tests. Read more about it on the
`papc documentation <https://acc-py.web.cern.ch/gitlab/pelson/papc/docs/stable/>`_.

.. index:: tests/
.. _tests_folder

tests/
^^^^^^
This folder contains the automated tests for your app. It already contains some basic tests to ensure your setup is
correct, and they will be run on GitLab CI every time you push code to your repository.

In the case of the demo code, they tests the demo application, making sure the SET command have an actual effect on
the simulated device, and other things. You can run your tests locally by executing::

    python -m pytest

To see the coverage report, type::

    python -m pytest --cov=<project_name>

.. note:: If the tests hang, probably Qt is swallowing errors without exiting. This can happen for the same reasons on
    GitLab CI. To see the stacktrace, re-run the tests as::

        python -m pytest --vv --log-cli-level=DEBUG

