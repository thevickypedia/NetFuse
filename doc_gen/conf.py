# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import pathlib
import sys

os.chdir(pathlib.Path(__file__).parent.parent)
sys.path.insert(0, str(pathlib.Path(__file__).parent.parent))

project = 'NetFuse'
copyright = '2023, Vignesh Rao'
author = 'Vignesh Rao'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.napoleon",  # certain styles of doc strings
    "sphinx.ext.autodoc",  # generates from doc strings
    "recommonmark",  # supports markdown integration
]

# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html#configuration
napoleon_google_docstring = True
napoleon_use_param = False

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
# https://www.sphinx-doc.org/en/master/usage/theming.html#builtin-themes
html_theme = "classic"
html_theme_options = {"body_max_width": "80%"}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Add docstrings from __init__ method
# This will also include __init__ docs from 'pydantic.BaseModel' and 'pydantic.BaseSettings'
# Reference: https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autoclass_content
# autoclass_content = "both"

# Include private methods/functions
# Reference: https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autodoc_default_options
autodoc_default_options = {
    "members": True,
    "undoc-members": True,
    "private-members": True,
}

# Add support to mark down files in sphinx documentation
# Reference: https://www.sphinx-doc.org/en/1.5.3/markdown.html
source_suffix = {
    ".rst": "restructuredtext",
    ".txt": "markdown",
    ".md": "markdown",
}

# Retain the function/member order
# Reference: https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html#confval-autodoc_member_order
autodoc_member_order = "bysource"

# Make left pane scroll
html_css_files = ["static.css"]
