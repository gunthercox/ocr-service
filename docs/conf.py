"""
Configuration file for the Sphinx documentation builder
"""

import os
import sys


sys.path.insert(0, os.path.abspath('..'))

project = 'ocr-service'
copyright = '2026, Gunther Cox'
author = 'Gunther Cox'
release = '1.1.2'

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
]

html_static_path = ['_static']
templates_path = ['_templates']

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

# Intersphinx mapping for Flask
intersphinx_mapping = {
    'flask': ('https://flask.palletsprojects.com/en/latest/', None),
}

# Enable source link in HTML output
html_show_sourcelink = True
html_copy_source = True
