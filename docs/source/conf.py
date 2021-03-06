import datetime
import pkg_resources

project = "BE/BI PyQt5 Tutorial"
author = "Sara Zanzottera (BE-BI-SW)"
version = "0.0.1"

copyright = "{0}, CERN".format(datetime.datetime.now().year)


# -- General configuration ----------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'acc_py_sphinx.theme',
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.doctest',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.autosectionlabel',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = "acc_py"
html_title = "The BE/BI PyQt5 Tutorial"
html_short_title = "PyQt5 Tutorial"
html_logo = '../images/pyqt-logo-inverted-smaller.png'
html_favicon = '../images/pyqt-logo.png'

# Static files directories
html_static_path = ["../images", "../videos"]

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
# html_static_path = ["_static"]
html_show_sphinx = False
html_show_sourcelink = True


# -- Options for sphinx.ext.autosummary

autosummary_generate = True
autosummary_imported_members = True


# -- Options for sphinx.ext.autosectionlabel

autosectionlabel_prefix_document = True
autosectionlabel_maxdepth = 10
