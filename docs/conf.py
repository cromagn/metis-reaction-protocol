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
