# Configuration file for the Sphinx documentation builder.

project = 'ocr-service'
copyright = '2026, Your Name'
author = 'Your Name'
release = '0.1.0'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
]

autodoc_default_options = {
    'members': True,
    'undoc-members': True,
    'private-members': False,
    'special-members': False,
    'inherited-members': True,
    'show-inheritance': True,
}

exclude_patterns = ['_build']

html_theme = 'alabaster'

import os
import sys

sys.path.insert(0, os.path.abspath('..'))

# Intersphinx mapping for Flask
intersphinx_mapping = {
    'flask': ('https://flask.palletsprojects.com/en/latest/', None),
}
