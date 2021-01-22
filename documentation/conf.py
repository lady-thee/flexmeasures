# -*- coding: utf-8 -*-
#
# Configuration file for the Sphinx documentation builder.
#
# This file does only contain a selection of the most common options. For a
# full list see the documentation:
# http://www.sphinx-doc.org/en/stable/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from datetime import datetime

from humanize import naturaldelta

from flexmeasures.app import create as create_app
from flexmeasures.ui.utils.view_utils import get_git_description

sys.path.insert(0, os.path.abspath(".."))
flexmeasures_app = create_app()


# -- Project information -----------------------------------------------------

project = flexmeasures_app.config.get("FLEXMEASURES_PLATFORM_NAME")
copyright = f"{datetime.now().year}, Seita Energy Flexibility, developed in partnership with A1 Engineering, South Korea"
author = "Seita B.V."

# The short X.Y version
git_version, git_commits_since, git_hash = get_git_description()
version = f"{git_version} + {git_commits_since} commits (revision {git_hash})"
# The full version, including alpha/beta/rc tags
release = version

rst_prolog = f"""
    .. |FLEXMEASURES_PLATFORM_NAME| replace:: {flexmeasures_app.config.get("FLEXMEASURES_PLATFORM_NAME")}
    .. |FLEXMEASURES_PLANNING_HORIZON| replace:: {naturaldelta(flexmeasures_app.config.get("FLEXMEASURES_PLANNING_HORIZON"))}
    .. |FLEXMEASURES_PLANNING_TTl| replace:: {naturaldelta(flexmeasures_app.config.get("FLEXMEASURES_PLANNING_TTL"))}
"""

# -- General configuration ---------------------------------------------------

# If your documentation needs a minimal Sphinx version, state it here.
#
# needs_sphinx = '1.0'

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.coverage",
    "sphinx.ext.imgmath",
    "sphinx.ext.ifconfig",
    "sphinxcontrib.autohttp.flask",
    "sphinxcontrib.autohttp.flaskqref",
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = ['.rst', '.md']
source_suffix = ".rst"

# The master toctree document.
master_doc = "index"

# The language for content autogenerated by Sphinx. Refer to documentation
# for a list of supported languages.
#
# This is also used if you do content translation via gettext catalogs.
# Usually you set "language" from the command line for these cases.
language = None

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path .
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]
if flexmeasures_app.config.get("FLEXMEASURES_MODE", "") == "demo":
    exclude_patterns.append("api/*.rst")
if flexmeasures_app.config.get("FLEXMEASURES_MODE", "") != "play":
    exclude_patterns.append("api/simulation.rst")

# Todo: these are not mature enough yet for release
exclude_patterns.append("int/*.rst")
exclude_patterns.append("qa/*.rst")
exclude_patterns.append("tut/*.rst")

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = "sphinx"


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster'
html_theme = "sphinx_rtd_flexmeasures_theme"
html_theme_path = ["_themes"]

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
#
# html_theme_options = {}

# Add any paths that contain custom _static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin _static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ["_static"]

# Custom sidebar templates, must be a dictionary that maps document names
# to template names.
#
# The default sidebars (for documents that don't match any pattern) are
# defined by theme itself.  Builtin themes are using these templates by
# default: ``['localtoc.html', 'relations.html', 'sourcelink.html',
# 'searchbox.html']``.
#
# html_sidebars = {}


# -- Options for HTMLHelp output ---------------------------------------------

# Output file base name for HTML help builder.
htmlhelp_basename = "FLEXMEASURESdoc"


# -- Options for LaTeX output ------------------------------------------------

latex_elements = {
    # The paper size ('letterpaper' or 'a4paper').
    #
    # 'papersize': 'letterpaper',
    # The font size ('10pt', '11pt' or '12pt').
    #
    # 'pointsize': '10pt',
    # Additional stuff for the LaTeX preamble.
    #
    # 'preamble': '',
    # Latex figure (float) alignment
    #
    # 'figure_align': 'htbp',
}

# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title,
#  author, documentclass [howto, manual, or own class]).
latex_documents = [
    (
        master_doc,
        f"{project}.tex",
        f"{project} Documentation",
        author,
        "manual",
    )
]


# -- Options for manual page output ------------------------------------------

# One entry per manual page. List of tuples
# (source start file, name, description, authors, manual section).
man_pages = [(master_doc, project, f"{project} Documentation", [author], 1)]


# -- Options for Texinfo output ----------------------------------------------

# Grouping the document tree into Texinfo files. List of tuples
# (source start file, target name, title, author,
#  dir menu entry, description, category)
texinfo_documents = [
    (
        master_doc,
        project,
        f"{project} Documentation",
        author,
        project,
        f"The {project} Platform is a tool for scheduling flexible energy actions on behalf of the connected asset owners.",
        "Miscellaneous",
    )
]


# -- Extension configuration -------------------------------------------------

# -- Options for intersphinx extension ---------------------------------------

# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {"https://docs.python.org/": None}

# -- Options for ifconfig extension ---------------------------------------


def setup(sphinx_app):
    """
    Here you can set config variables for Sphinx or even pass config variables from FlexMeasures to Sphinx.
    For example, to display content depending on FLEXMEASURES_MODE (specified in the FlexMeasures app's config.py),
    place this in one of the rst files:

    .. ifconfig:: FLEXMEASURES_MODE == "play"

        We are in play mode.

    """

    # sphinx_app.add_config_value('RELEASE_LEVEL', 'alpha', 'env')
    sphinx_app.add_config_value(
        "FLEXMEASURES_MODE", flexmeasures_app.config.get("FLEXMEASURES_MODE", ""), "env"
    )
    sphinx_app.add_css_file("css/custom.css")
