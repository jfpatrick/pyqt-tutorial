PyQt5 Mega Tutorial for BE-BI
-----------

Python API and small CLI tool to query the CERN LDAP personnel database.

Prerequisites
-------------
PyPhoneBook uses ``python-ldap``, which requires a few packages to be
available on the system.

For CentOS7, type::

    sudo yum install -y openldap-devel python-devel

For other distros, please refer to the
`python-ldap documentation <https://www.python-ldap.org/en/python-ldap-3.2.0/>`_.


Installation
------------


Using the `acc-py Python package index
<https://wikis.cern.ch/display/ACCPY/Getting+started+with+acc-python#Gettingstartedwithacc-python-OurPythonPackageRepositoryrepo>`_
``pyphonebook`` can be pip installed with::

   pip install pyphonebook

You can verify the installation was successful by typing::

    pyphonebook

You should see a help message.


Quick start
-----------

As a CLI tool
^^^^^^^^^^^^^

The CLI interface is quite simple. Type::

    pyphonebook

to have an overview of the parameters you can use for the search,
plus a few options (sorting and rendering).

Note that the CLI interface is not meant to be used in scripts.
To integrate PyPhoneBook with other tools, please consider using
it as a Python dependency.

As a Python package
^^^^^^^^^^^^^^^^^^^
The Python API are quite richer than the CLI interface.

Here is a simple example of usage::

    from pyphonebook import PhoneBook

    pb = PhoneBook()
    results = pb.search_by_login_name("your_login_name_here")

    if len(results) == 0:
        print("No results for this username")

    for result in results:
        if result.parsing_failed:
            print("The parsing of this entry failed, but we can see why:")
            print(" - ", result.exception_raised)
            print("And we can see the original, raw data:")
            print(result.raw_data)
        else:
            print(" - Pretty printed version with most meaningful fields:")
            print(result)
            print("\n")
            print(" - Machine friendly output as JSON:")
            print(result.to_json(indent=4, include_raw=False))
            print("\n---------------------------------------------------------")

Please refer to the
`ReadTheDocs documentation <https://acc-py.web.cern.ch/gitlab/szanzott/pyphonebook/docs/master/>`_
for a complete description of the API.

Read the code
^^^^^^^^^^^^^

In case of doubt, feel free to dive into the code. The entire codebase is really
small and heavily commented, so that it can be understood by non experts too.

Also, ``python-ldap`` takes care of most of the complexity related to LDAP servers querying,
so with the exception of the pagination loop, the rest of the query code is almost trivial.

Contribute
----------

Please report issues and make PR on the `GitLab repository <https://gitlab.cern.ch/szanzott/pyphonebook>`_.

Documentation contents
----------------------

.. toctree::
    :maxdepth: 1
    :hidden:

    self

.. toctree::
    :caption: Reference docs
    :maxdepth: 1

    api
    genindex

