import os
import sys
from datetime import datetime

# Aggiungi la root del repo al path (se un giorno servirà)
sys.path.insert(0, os.path.abspath(".."))

project = "Metis BLE Protocol Reverse Engineering"
author = "cromagn"
copyright = f"{datetime.now().year}, {author}"

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.githubpages",
]

templates_path = ["_templates"]
exclude_patterns = []

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]

def setup(app):
    app.add_config_value('google_site_verification', 'HynwfZ55tPg46y8pYrstjyaT5_hbhMYEe8bfRqrAvLA', 'html')
    def add_google_tag(app, pagename, templatename, context, doctree):
        metatag = f'<meta name="google-site-verification" content="{app.config.google_site_verification}" />'
        context['metatags'] = context.get('metatags', '') + metatag
    app.connect('html-page-context', add_google_tag)
