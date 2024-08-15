# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
project = 'FastAPI Contacts Project'
copyright = '2024, Andriy Sydor'
author = 'Andriy Sydor'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    'sphinx.ext.autodoc',      # Додаємо autodoc для підтримки автоматичної документації
    'sphinx.ext.napoleon',     # Додаємо підтримку стилів docstring Google та NumPy
    'sphinx.ext.viewcode',     # Додаємо можливість перегляду вихідного коду у документації
]

templates_path = ['_templates']
exclude_patterns = []

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']
