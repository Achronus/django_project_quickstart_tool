import os
import sys

from config import *


# Change venv activation depending on OS
if sys.platform.startswith("win"):
    VENV = "venv\\Scripts"
else:
    VENV = "venv/bin/"


# Setup assets directory name and child directory names
SETUP_ROOT_ASSETS_NAME = 'setup_assets'
SETUP_ROOT_ASSETS_ROOT_FOLDER = 'root'
SETUP_ROOT_ASSETS_STATIC_FOLDER = 'static'
SETUP_ROOT_ASSETS_TEMPLATE_FOLDER = 'templates'

SETUP_FIRSTAPP_DIR = 'firstapp'

# Setup assets filepaths
SETUP_ROOT_DIR = os.path.dirname(os.path.join(os.getcwd(), SETUP_ROOT_ASSETS_NAME))
SETUP_ASSETS_DIR = os.path.join(SETUP_ROOT_DIR, SETUP_ROOT_ASSETS_NAME)
SETUP_ASSETS_ROOT_DIR = os.path.join(SETUP_ASSETS_DIR, SETUP_ROOT_ASSETS_ROOT_FOLDER)
SETUP_ASSETS_STATIC_DIR = os.path.join(SETUP_ASSETS_DIR, SETUP_ROOT_ASSETS_STATIC_FOLDER)
SETUP_ASSETS_TEMPLATE_DIR = os.path.join(SETUP_ASSETS_DIR, SETUP_ROOT_ASSETS_TEMPLATE_FOLDER)


# Settings and url file paths associated to STARTPROJECT
ROOT_SETTINGS_PATH = os.path.join(SETTINGS_DIR, "settings.py")
ROOT_URLS_PATH = os.path.join(SETTINGS_DIR, "urls.py")


# Primary static and template files associated to FIRSTAPP 
FIRSTAPP_URLS_PATH = os.path.join(FIRSTAPP_DIR, "urls.py")
FIRSTAPP_VIEWS_PATH = os.path.join(FIRSTAPP_DIR, "views.py")

ROOT_STATIC_FOLDER_URL = os.path.join(FIRSTAPP_DIR, 'static')
ROOT_TEMPLATE_FOLDER_URL = os.path.join(FIRSTAPP_DIR, 'templates')


# JS library urls
FLOWBITE_FILENAME = 'flowbite.min.js'
HTMX_FILENAME = 'htmx.min.js'
ALPINE_FILENAME = 'alpine.min.js'

FLOWBITE_URL = f'node_modules/flowbite/dist/{FLOWBITE_FILENAME}'
HTMX_URL = f'https://unpkg.com/htmx.org/dist/{HTMX_FILENAME}'
ALPINE_URL = f'node_modules/alpinejs/dist/cdn.min.js'
