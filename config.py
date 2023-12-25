# EDITABLE CONSTANTS
SETTINGS_DIR = "config"  # projectapp
FIRSTAPP_DIR = "core"

STATIC_URL = 'static/'
STATIC_ROOT_DIR = 'public'

# Superuser details
SUPERUSER_NAME = 'admin'
SUPERUSER_EMAIL = 'admin@example.com'
SUPERUSER_PASSWORD = 'admin'

# Pip packages to install
PIP_PACKAGES = [
    "django", 
    "django-compressor", 
    "django-browser-reload", 
    "django-htmx", 
    "python-dotenv"
]

# TEMPLATES DIRS additions
TEMPLATES_DIRS_ADDITIONS = [
    "os.path.join(BASE_DIR, 'templates')"
]

# INSTALLED_APPS setting additions
INSTALLED_APPS_3RDPARTY = [
    "compressor",
    "django_htmx", 
    "django_browser_reload"
]
INSTALLED_APPS_LOCAL = [
    "core"
]

# MIDDLEWARE setting additions
MIDDLEWARE_3RDPARTY_BOTTOM = [
    "django_browser_reload.middleware.BrowserReloadMiddleware",
    "django_htmx.middleware.HtmxMiddleware"
]

# STATICFILES setting additions
NEW_STATICFILES_DIRS = [
    # "os.path.join(BASE_DIR, 'static')"  # example
]

STATICFILES_DEFAULT_FINDERS = [
    "django.contrib.staticfiles.finders.FileSystemFinder",
    "django.contrib.staticfiles.finders.AppDirectoriesFinder"
]
NEW_STATICFILES_3RDPARTY_FINDERS = [
    "compressor.finders.CompressorFinder"
]

# .env file additional parameters
ENV_FILE_ADDITIONAL_PARAMS = [
    # f'DATABASE_NAME={DB_NAME}'  # example
]
