###############################################################################
# Auto-generated by `jupyter-book config`
# If you wish to continue using _config.yml, make edits to that file and
# re-generate this one.
###############################################################################
apidoc_module_dir = "../src"
author = "Development Data Group"
bibtex_bibfiles = ["bibliography.bib"]
comments_config = {"hypothesis": False, "utterances": False}
copyright = "2023"
exclude_patterns = ["**.ipynb_checkpoints", ".DS_Store", "Thumbs.db", "_build"]
extensions = [
    "sphinx_togglebutton",
    "sphinx_copybutton",
    "myst_nb",
    "jupyter_book",
    "sphinx_thebe",
    "sphinx_comments",
    "sphinx_external_toc",
    "sphinx.ext.intersphinx",
    "sphinx_design",
    "sphinx_book_theme",
    "sphinxcontrib.bibtex",
    "sphinx_jupyterbook_latex",
    "sphinx.ext.napoleon",
    "sphinxcontrib.apidoc",
]
external_toc_exclude_missing = True
external_toc_path = "_toc.yml"
extra_extensions = ["sphinxcontrib.apidoc"]
html_baseurl = "https://worldbank.github.io/blackmarblepy"
html_favicon = "images/favicon.ico"
html_last_updated_fmt = "%b %d, %Y"
html_logo = "images/logo.png"
html_show_copyright = False
html_sourcelink_suffix = ""
html_theme = "sphinx_book_theme"
html_theme_options = {
    "search_bar_text": "Search this book...",
    "launch_buttons": {
        "notebook_interface": "classic",
        "binderhub_url": "",
        "jupyterhub_url": "",
        "thebe": False,
        "colab_url": "",
    },
    "path_to_docs": "",
    "repository_url": "https://github.com/worldbank/blackmarblepy",
    "repository_branch": "main",
    "extra_footer": "",
    "home_page_in_toc": False,
    "announcement": "",
    "analytics": {"google_analytics_id": "G-ZWF69GP65G"},
    "use_repository_button": True,
    "use_edit_page_button": True,
    "use_issues_button": True,
}
html_title = ""
latex_engine = "pdflatex"
myst_enable_extensions = [
    "colon_fence",
    "dollarmath",
    "linkify",
    "substitution",
    "tasklist",
]
myst_url_schemes = ["mailto", "http", "https"]
nb_execution_allow_errors = False
nb_execution_cache_path = ""
nb_execution_excludepatterns = []
nb_execution_in_temp = False
nb_execution_mode = "off"
nb_execution_timeout = 30
nb_output_stderr = "show"
numfig = True
pygments_style = "sphinx"
suppress_warnings = ["myst.domains"]
use_jupyterbook_latex = True
use_multitoc_numbering = True
