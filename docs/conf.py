"""
Configuration file for the Sphinx documentation builder
"""

import os
import sys
import sphinx_sitemap


sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('.'))

project = 'ocr-service'
copyright = '2026, Gunther Cox'
author = 'Gunther Cox'
release = '1.2.2'

# SEO Configuration
html_baseurl = 'https://gunthercox.com/ocr-service/'
html_title = 'OCR API Documentation - Tesseract & PaddleOCR REST Service'
html_short_title = 'OCR Service Docs'
language = 'en'
html_use_index = True

# Sitemap configuration for sphinx-sitemap
sitemap_url_scheme = "{link}"

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    '_ext.canonical',
    '_ext.github',
    '_ext.meta_descriptions',
    'sphinx_sitemap',
]

html_static_path = ['_static']
templates_path = ['_templates']

# Copy robots.txt to the output
html_extra_path = ['robots.txt']

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

html_theme_options = {
    'github_user': 'gunthercox',
    'github_repo': 'ocr-service',
    'github_button': True,
    'github_banner': True,
    'github_type': 'star',
}
