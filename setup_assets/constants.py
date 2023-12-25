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


# Settings and url file paths associated to STARTPROJECT
ROOT_SETTINGS_PATH = os.path.join(SETTINGS_DIR, "settings.py")
ROOT_URLS_PATH = os.path.join(SETTINGS_DIR, "urls.py")


# Primary static and template files associated to FIRSTAPP 
FIRSTAPP_URLS_PATH = os.path.join(FIRSTAPP_DIR, "urls.py")
FIRSTAPP_VIEWS_PATH = os.path.join(FIRSTAPP_DIR, "views.py")

ROOT_STATIC_FOLDER_URL = os.path.join(FIRSTAPP_DIR, 'static')
ROOT_TEMPLATE_FOLDER_URL = os.path.join(FIRSTAPP_DIR, 'templates')

