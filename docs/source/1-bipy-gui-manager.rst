.. index:: Setup a New Project
.. _setup_new_project:

=================
Setup New Project
=================

New PyQt Expert GUIs in BI should be build according to a predefined structure, which you can setup by using the
`BI Python Expert GUI Manager <https://gitlab.cern.ch/bisw-python/bipy-gui-manager>`_


.. index:: BI Python Expert GUI Manager
.. index:: bipy-gui-manager
.. _bipy-gui-manager:

BI Python Expert GUI Manager (bipy-gui-manager)
===============================================

`bipy-gui-manager` is a small Python utility to create a project template (think of it as a Java archetype)
for an Expert GUI PyQt5 application. It's specifically tuned for BI Expert GUIs.

How do I use it?
================

Open a terminal on a virtual Linux machine with TN access and type::

    /user/bdisoft/development/python/gui/bipy-gui-manager create-project

The script will guide you through the configuration of a new project. The script itself will describe most
of what's going on and the next steps after the install, so feel free to go ahead and try it out before proceeding
with this tutorial.

After running ``bipy-gui-manager`` you already have a running application. To start it, type in the console
the name of your project (the one you gave to ``bipy-gui-manager`` while creating the project). You should see the
frame with a dummy application in the center, like this:

.. raw:: html

         <img src="_static/application-template.png" />

or a smaller window with an error. In the latter case, please report the error
to the maintainers.

In the next section we are going to review the project structure, so skip ahead if you're interested.


.. index:: Aliasing and linking ``bipy-gui-manager``
.. _bipy-gui-manager_aliasing:

How to avoid using the full path?
=================================

If you plan to use this tool again in the future, you can make ``bipy-gui-manager`` available in your console without
having to type the full path. To do so, use one of the following strategies:

    * **Alias it**
      This method will not modify your ``PATH`` and won't create symlinks, but requires you to edit your
      ``~/.bashrc``. Add the following line to your ``~/.bashrc``::

            alias bipy-gui-manager="/user/bdisoft/development/python/gui/bipy-gui-manager"


    * **Add it to PATH under ~/.local/bin**
      This method assumes that ``~/.local/bin`` is already in your ``PATH``, or that you can add it yourself.
      It will create a symlink to ``bipy-gui-manager`` under ``~/.local/bin``. Simply type::

            ln -s /user/bdisoft/development/python/gui/bipy-gui-manager ~/.local/bin/bipy-gui-manager

    * **Add it to PATH under '/usr/local/bin'**
      This method assumes that ``/usr/local/bin`` is already in your ``PATH``, which is true for most users, and
      that you can perform operations as ``sudo``. It will create a symlink to ``bipy-gui-manager`` under
      ``/usr/local/bin``. Simply type::

            sudo ln -s /user/bdisoft/development/python/gui/bipy-gui-manager /usr/local/bin/bipy-gui-manager

.. index:: bipy-gui-manager Advanced Usage
.. _bipy-gui-manager_advanced:

Advanced Usage
==============

``bipy-gui-manager`` has a CLI interface that allows for some degree of automation. Type::

    bipy-gui-manager--help

in the console for an overview of the main sub-commands, or::

    bipy-gui-manager create-project --help

for a complete description of create-project's CLI interface.

.. index:: bipy-gui-manager Contacts
.. _bipy-gui-manager_contacts:

Contacts
========
For questions or bug reports about ``bipy-gui-manager``, contact Sara Zanzottera or Steen Jensen.


.. index:: bipy-gui-manager FAQ
.. bipy-gui-manager_faq:

FAQ
===

*TODO*
