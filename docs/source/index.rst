.. index:: Home
.. _home

==============
PyQt5 Tutorial
==============

Welcome to the PyQt5 Tutorial for BE/BI!

We will cover the current infrastructure for PyQt development at CERN, with special focus on the tools
provided by BE/CO and the best practices we defined for BE/BI Expert GUIs.

This tutorial assumes a decent knowledge of Python, and in general will not dive too much into pure
Python details. In some cases, the tutorial will help beginners by offering links to external
resources that cover that specific topic.
However, please stop and do a bit of research if some concept confuses you.

All the pages are equipped with videos, runnable code and descriptions.
They mostly cover the same content, i.e. the videos cover the same materials as their host page,
and they both refer to the same code.


.. index:: External Tutorials
.. _external_tutorials:

External Resources
==================

Here is a list of some good tutorials on PyQt that can help you get started. If you know any other, please send the
link to Sara Zanzottera or Steen Jensen and it will be added to the list.

Web Tutorials
-------------

 * **LikeGeeks PyQt5 Tutorial**: https://likegeeks.com/pyqt5-tutorial/ A very concise, yet comprehensive PyQt5 tutorial.
   Covers Qt Designer and more complex widgets like ComboBoxes and Tables.
   A recommended resource for getting started quickly.

|

 * **LearnPyQt**: https://www.learnpyqt.com/ Longer, more descriptive PyQt5 tutorial with videos and example apps.
   Note that part of the tutorial require you to login and/or buy the course,
   however the free content is still very useful to begin with.

    .. warning:: Ignore the section on Qt Creator: it is not supported in our infrastructure.
                 We use Qt Designer instead.

   Some examples of free content from this course:

    - Creating your first app with PyQt: https://www.learnpyqt.com/courses/start/creating-your-first-window/
    - Signals, Slots & Events: https://www.learnpyqt.com/courses/start/signals-slots-events/
    - Widgets: https://www.learnpyqt.com/courses/start/basic-widgets/
    - How to use Qt Designer: https://www.learnpyqt.com/courses/qt-creator/qt-designer-gui-layout/
    - Dialogs and Alerts: https://www.learnpyqt.com/courses/start/dialogs/
    - The Model/View architecture: https://www.learnpyqt.com/courses/model-views/modelview-architecture/

   It also offers a few small apps that can be used as examples: https://github.com/learnpyqt/15-minute-apps

|

 * **fman's PyQt5 tutorial**: https://build-system.fman.io/pyqt5-tutorial. This is more of a reference page than a
   tutorial. Useful to pinpoint all the crucial topics you have to be aware of to develop PyQt apps.
   It also provides a repository with a number of example applications: https://github.com/pyqt/examples

   Note: does not cover Qt Designer.

|

 * **RealPython's PyQt5 tutorial**: https://realpython.com/python-pyqt-gui-calculator/ Another good tutorial that
   guides you though the process of building a calculator application. Although it mentions Qt Designer, it does not
   uses it, nor it explains how it works.

|

 * **ZetCodes's PyQt5 Tutorial**: http://zetcode.com/gui/pyqt5/ Old-fashioned website providing a few hands-on examples
   of PyQt5 applications. Does not cover Qt Designer and produces all the interfaces in code, which is not recommended.
   However it can be a useful reference on some less-known topics.
   As a plus, it offers also a `Python tutorial <http://zetcode.com/lang/python/>`_ for the very beginners.

|

 * **Data Flair's PyQt5 Tutorial**: https://data-flair.training/blogs/python-pyqt5-tutorial/ Another quick tutorial
   that covers the basics in a series of very small example applications. Does not cover Qt Designer.

Video Tutorials
---------------

 * **Tech With Tim's PyQt5 Introduction:** https://www.youtube.com/playlist?list=PLzMcBGfZo4-lB8MZfHPLTEHO9zJDDLpYj
   Covers mostly the very basics, and although Windows specific, it contains some very valuable explanations.
   It has a companion website with the code, that you can use to follow through:
   https://techwithtim.net/tutorials/pyqt5-tutorial/basic-gui-application/

Books (Available at the CERN Online Library)
--------------------------------------------

 * **Qt5 Python GUI Programming Cookbook** by B.M. Harwani:
   https://learning.oreilly.com/library/view/qt5-python-gui/9781788831000/

|

 * **Mastering GUI Programming with Python** by A. D. Moore: https://cds.cern.ch/record/2685778?ln=en
   The most important chapters
   `can be downloaded as PDF here <https://wikis.cern.ch/download/attachments/122078447/Mastering_GUI_Programming_with_Python.zip?version=1&modificationDate=1590396774000&api=v2>`_
   (downloaded with permission from the library's link above).


Example Code
------------

PyQt5 ships with some embedded examples, which usually are found in your local
``venv/lib/python3.6.site-packages/PyQt5/examples`` folder. In the shared PyQt5 installation the examples
seems to have been removed, but you can still check them out at this repo:
https://github.com/baoboa/pyqt5/tree/master/examples


Reference Documentation (Advanced users)
----------------------------------------

 * **Riverbank's PyQt5 Reference Guide**: https://www.riverbankcomputing.com/static/Docs/PyQt5/
   Cover in extreme detail the inner workings of PyQt5 and all the technical details. Might be useful for debugging.

|

 * **Qt5 Documentation**: https://doc.qt.io/qt-5/classes.html https://doc.qt.io/qt-5/qtmodules.html
   PyQt API are in most cases an exact clone of Qt5 API. Therefore Qt5 Docs are officially the reference
   documentation for PyQt5 as well.



Contribute
==========

Any form of contribution is welcome!

Please report issues or ideas and make PR on the
`GitLab repository <https://gitlab.cern.ch/szanzott/pyqt-mega-tutorial-for-be-bi>`_,
or contact Sara Zanzottera or Steen Jensen.


.. toctree::
    :maxdepth: 1
    :hidden:

    self
    fast/index
    complete/index
    genindex

