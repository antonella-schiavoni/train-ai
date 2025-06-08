"""Sphinx configuration."""
project = "Train Ai"
author = "Antonella Schiavoni"
copyright = "2025, Antonella Schiavoni"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx_click",
    "myst_parser",
]
autodoc_typehints = "description"
html_theme = "furo"
