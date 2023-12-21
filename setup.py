import os
import shutil
import subprocess
import sys
from functools import wraps

# Change venv activation depending on OS
if sys.platform.startswith("win"):
    VENV = "venv\\Scripts"
else:
    VENV = "venv/bin/"


#-------------------------------------------------------------------------
# EDITABLE CONSTANTS
#-------------------------------------------------------------------------
SETTINGS_DIR = "config"
FIRSTAPP_DIR = "core"

# Settings and url file paths associated to STARTPROJECT
ROOT_SETTINGS_PATH = os.path.join(SETTINGS_DIR, "settings.py")
ROOT_URLS_PATH = os.path.join(SETTINGS_DIR, "urls.py")

STATIC_URL = 'static/'
STATIC_ROOT_DIR = 'public'

# Primary static and template files associated to FIRSTAPP 
FIRSTAPP_URLS_PATH = os.path.join(FIRSTAPP_DIR, "urls.py")
FIRSTAPP_VIEWS_PATH = os.path.join(FIRSTAPP_DIR, "views.py")

ROOT_STATIC_FOLDER_URL = os.path.join(FIRSTAPP_DIR, 'static')
ROOT_TEMPLATE_FOLDER_URL = os.path.join(FIRSTAPP_DIR, 'templates')

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
    "os.path.join(BASE_DIR, 'templates'),"
]

# INSTALLED_APPS setting additions
INSTALLED_APPS_3RDPARTY = [
    "'compressor',",
    "'django_htmx',", 
    "'django_browser_reload',"
]
INSTALLED_APPS_LOCAL = [
    "'core',"
]

# MIDDLEWARE setting additions
MIDDLEWARE_3RDPARTY_BOTTOM = [
    "'django_browser_reload.middleware.BrowserReloadMiddleware',",
    "'django_htmx.middleware.HtmxMiddleware',"
]

# STATICFILES setting additions
NEW_STATICFILES_DIRS = [
    # "os.path.join(BASE_DIR, 'static'),",  # example
]

STATICFILES_DEFAULT_FINDERS = [
    "'django.contrib.staticfiles.finders.FileSystemFinder',",
    "'django.contrib.staticfiles.finders.AppDirectoriesFinder',"
]
NEW_STATICFILES_3RDPARTY_FINDERS = [
    "'compressor.finders.CompressorFinder',"
]
#-------------------------------------------------------------------------


# Helper functions
def __get_config_list_content(start_marker: str, end_marker: str, path: os.path) -> str:
    """Helper function for `update_installed_apps()` and `update_middleware()`. Retrieves content in a `path` between `start_marker` and `end_marker`."""
    with open(path, "r") as file:
        content = file.readlines()

    # Get start and end markers
    for _, line in enumerate(content):
        if line.startswith(start_marker):
            start_marker = line

        if line.startswith(end_marker):
            end_marker = line
            break


    with open(path, "r") as file:
        content = file.read()     

    start_idx = content.find(start_marker)
    end_idx = content.find(end_marker, start_idx)

    content_str = content[start_idx:end_idx].strip()
    return content_str


def __list_content_update(old_content: str, additions: list[str]) -> None:
    """Helper function for `update_installed_apps()` and `update_middleware()`. Updates a list of content given the `old_content` and a list of `additions`."""
    new_content = old_content
    for item in additions:
        new_content += ''.join(f"    {item}\n")
    
    @readwrite_file(path=ROOT_SETTINGS_PATH)
    def update_content(content: str) -> str:
        return content.replace(
            old_content,
            new_content.strip(),
            1
        )

    update_content()


# Decorators
def readwrite_lines(path: str):
    """Decorator for using 'file.readlines()' and updating content to it."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with open(path, "r") as file:
                content = file.readlines()

            for i, line in enumerate(content):
                content = func(content, i, line, *args, **kwargs)

            with open(path, "w") as file:
                file.writelines(content)

        return wrapper
    return decorator


def readwrite_file(path: str):
    """Decorator for using 'file.read()' and writing replacement content to it."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            with open(path, "r") as file:
                content = file.read()

            content = func(content, *args, **kwargs)

            with open(path, "w") as file:
                file.writelines(content)

        return wrapper
    return decorator


def copy_files(file_or_dir: str, middle_dest: str = ''):
    """Decorator for copying files from one location to another.
    
    :param file_or_dir: (str) a file or directory to copy over stored in `os.getcwd`
    :param middle_dest: (str, optional) a middle destination path added before the `file_or_dir` and after the `os.getcwd()`
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            project_root_dir = os.getcwd()
            parent_dir = os.path.dirname(project_root_dir)
            src_path = os.path.join(parent_dir, file_or_dir)
            dest_path = os.path.join(project_root_dir, middle_dest, file_or_dir)

            func(src_path, dest_path, *args, **kwargs)

        return wrapper
    return decorator


# Setup functions
def create_root_directory(directory_name: str) -> None:
    os.makedirs(directory_name)
    os.chdir(directory_name)


def create_virtual_environment() -> None:
    subprocess.run(["python", "-m", "venv", "venv"])


def install_packages() -> None:
    subprocess.run([os.path.join(VENV, "pip"), "install", "--upgrade", "pip"])
    subprocess.run([os.path.join(VENV, "pip"), "install", *PIP_PACKAGES])


def create_requirements_txt() -> None:
    with open("requirements.txt", "w") as file:
        subprocess.Popen([os.path.join(VENV, "pip"), "freeze"], stdout=file)


def run_django_startproject() -> None:
    subprocess.run([os.path.join(VENV, "django-admin"), "startproject", SETTINGS_DIR, "."])
    subprocess.run([os.path.join(VENV, "python"), "manage.py", "startapp", FIRSTAPP_DIR])


def make_static_dirs() -> None:
    os.makedirs(os.path.join(ROOT_STATIC_FOLDER_URL, "css"))
    os.makedirs(os.path.join(ROOT_STATIC_FOLDER_URL, "js"))
    os.makedirs(os.path.join(ROOT_STATIC_FOLDER_URL, "imgs"))


def create_input_css() -> None:
    with open(os.path.join(ROOT_STATIC_FOLDER_URL, "css", "input.css"), "w") as file:
        file.write("@tailwind base;\n")
        file.write("@tailwind components;\n")
        file.write("@tailwind utilities;\n")


def add_tailwindcss() -> None:
    subprocess.run(["npm", "install", "-D", "tailwindcss"], shell=True)
    subprocess.run(["npm", "install", "flowbite"], shell=True)

    # Create tailwind.config.js with required content
    with open("tailwind.config.js", "w") as file:
        file.write(
"""module.exports = {
    darkMode: 'class',
    content: [
        './**/*.html',
        './node_modules/flowbite/**/*.js',
    ],
    theme: {
        extend: {},
    },
    plugins: [
        require('flowbite/plugin'),
    ],
}
""")
    
    subprocess.run(["npx", "tailwindcss", "-i", "./core/static/css/input.css", "-o", "./core/static/css/output.css"], shell=True)

    # Update package.json for watching tailwindcss with 'dev' command
    @readwrite_file(path=os.path.join(os.getcwd(), "package.json"))
    def update_content(content: str) -> str:
        old_content = '"devDependencies": {'
        tw_css_cmd = "npx tailwindcss -i ./core/static/css/input.css -o ./core/static/css/output.css --watch"
        new_content = '"scripts": {\n\t\t"dev": ' + f'"{tw_css_cmd}"' + '\n\t},\n\t' + old_content

        content = content.replace(
            old_content,
            new_content,
            1
        )
        return content
    
    update_content()


def create_theme_toggle_script() -> None:
    with open(os.path.join(ROOT_STATIC_FOLDER_URL, "js", "theme-toggle.js"), "w") as file:
        file.write(
"""
if (localStorage.getItem('color-theme') === 'dark' || (
        !('color-theme' in localStorage) &&
        window.matchMedia('(prefers-color-scheme: dark)').matches)
    ) {
        document.documentElement.classList.add('dark');
    } else {
        document.documentElement.classList.remove('dark');
};

// When user explicity chooses light mode
localStorage.theme = 'light';

// When user explicity chooses dark mode
localStorage.theme = 'dark';

// When user chooses to respect OS preferences
localStorage.removeItem('theme');
""")


def create_core_template_base() -> None:
    os.makedirs(os.path.join(ROOT_TEMPLATE_FOLDER_URL, FIRSTAPP_DIR))
    with open(os.path.join(ROOT_TEMPLATE_FOLDER_URL, FIRSTAPP_DIR, "_base.html"), "w") as file:
        file.write(
"""<!-- templates/core/_base.html -->

{% load compress %}
{% load static %}

<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{% block title %}Homepage{% endblock title %}</title>

    {% compress css %}
    <link id="tw-css" rel="stylesheet" href="{% static 'css/output.css' %}">
    {% endcompress %}

    <script id="theme-toggle-js" src="{% static 'js/theme-toggle.js' %}"></script>
    <script id="htmx-js" src="https://unpkg.com/htmx.org@1.9.9"></script>
    <script id="alpine-js" defer src="https://cdn.jsdelivr.net/npm/alpinejs@3.x.x/dist/cdn.min.js"></script>

</head>

<body>
    {% include 'core/components/navbar.html' %}
    <div class="container mx-auto mt-4">
        {% block content %}
        {% endblock content %}
    </div>

    <script id="flowbite-js" src="https://cdnjs.cloudflare.com/ajax/libs/flowbite/2.2.0/flowbite.min.js"></script>
</body>

</html>
""")


def create_core_template_index() -> None:
    with open(os.path.join(ROOT_TEMPLATE_FOLDER_URL, FIRSTAPP_DIR, "index.html"), "w") as file:
        file.write(
"""<!-- templates/core/index.html -->

{% extends 'core/_base.html' %}

{% block content %}

<h1 x-data="{ message: 'I &#9829; Alpine' }" x-text="message" class="text-3xl text-red-500"></h1>
{% endblock content %}
""")


def create_core_navbar_component() -> None:
    os.makedirs(os.path.join(ROOT_TEMPLATE_FOLDER_URL, FIRSTAPP_DIR, "components", "nav"))
    with open(os.path.join(ROOT_TEMPLATE_FOLDER_URL, FIRSTAPP_DIR, "components", "navbar.html"), "w") as file:
        file.write(
"""<!-- templates/core/components/navbar.html -->
{% load static %}

<nav class="bg-white border-gray-200 dark:bg-gray-900">
  <div class="max-w-screen-xl flex flex-wrap items-center justify-between mx-auto p-4">
    <a href="https://flowbite.com/" class="flex items-center space-x-3 rtl:space-x-reverse">
        <img src="https://flowbite.com/docs/images/logo.svg" class="h-8" alt="Flowbite Logo" />
        <span class="self-center text-2xl font-semibold whitespace-nowrap dark:text-white">Flowbite</span>
    </a>
    <div class="flex items-center gap-3 md:order-2 space-x-3 md:space-x-0 rtl:space-x-reverse">
        <button type="button" class="text-white bg-blue-700 hover:bg-blue-800 focus:ring-4 focus:outline-none focus:ring-blue-300 font-medium rounded-lg text-sm px-4 py-2 text-center dark:bg-blue-600 dark:hover:bg-blue-700 dark:focus:ring-blue-800">Get started</button>
        <button type="button" class="flex text-sm bg-gray-800 rounded-full md:me-0 focus:ring-4 focus:ring-gray-300 dark:focus:ring-gray-600" id="user-menu-button" aria-expanded="false" data-dropdown-toggle="user-dropdown" data-dropdown-placement="bottom">
            <span class="sr-only">Open user menu</span>
            <img class="w-8 h-8 rounded-full" src="{% static 'imgs/avatar.svg' %}" alt="user photo">
        </button>
        {% include 'core/components/nav/mobile-nav.html' %}
    </div>
    <div class="items-center justify-between hidden w-full md:flex md:w-auto md:order-1" id="navbar-user">
        <ul class="flex flex-col font-medium p-4 md:p-0 mt-4 border border-gray-100 rounded-lg bg-gray-50 md:space-x-8 rtl:space-x-reverse md:flex-row md:mt-0 md:border-0 md:bg-white dark:bg-gray-800 md:dark:bg-gray-900 dark:border-gray-700">
        <li>
            <a href="#" class="block py-2 px-3 text-white bg-blue-700 rounded md:bg-transparent md:text-blue-700 md:p-0 md:dark:text-blue-500" aria-current="page">Home</a>
        </li>
        <li>
            <a href="#" class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700">About</a>
        </li>
        <li>
            <a href="#" class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700">Services</a>
        </li>
        <li>
            <a href="#" class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700">Pricing</a>
        </li>
        <li>
            <a href="#" class="block py-2 px-3 text-gray-900 rounded hover:bg-gray-100 md:hover:bg-transparent md:hover:text-blue-700 md:p-0 dark:text-white md:dark:hover:text-blue-500 dark:hover:bg-gray-700 dark:hover:text-white md:dark:hover:bg-transparent dark:border-gray-700">Contact</a>
        </li>
        </ul>
    </div>
  </div>
</nav>
""") 

    with open(os.path.join(ROOT_TEMPLATE_FOLDER_URL, FIRSTAPP_DIR, "components", "nav", "mobile-nav.html"), "w") as file:
        file.write(
"""<!-- templates/core/components/nav/mobile-nav.html -->

<div class="z-50 hidden my-4 text-base list-none bg-white divide-y divide-gray-100 rounded-lg shadow dark:bg-gray-700 dark:divide-gray-600" id="user-dropdown">
    <div class="px-4 py-3">
    <span class="block text-sm text-gray-900 dark:text-white">Bonnie Green</span>
    <span class="block text-sm  text-gray-500 truncate dark:text-gray-400">name@flowbite.com</span>
    </div>
    <ul class="py-2" aria-labelledby="user-menu-button">
    <li>
        <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white">Dashboard</a>
    </li>
    <li>
        <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white">Settings</a>
    </li>
    <li>
        <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white">Earnings</a>
    </li>
    <li>
        <a href="#" class="block px-4 py-2 text-sm text-gray-700 hover:bg-gray-100 dark:hover:bg-gray-600 dark:text-gray-200 dark:hover:text-white">Sign out</a>
    </li>
    </ul>
</div>
<button data-collapse-toggle="navbar-user" type="button" class="inline-flex items-center p-2 w-10 h-10 justify-center text-sm text-gray-500 rounded-lg md:hidden hover:bg-gray-100 focus:outline-none focus:ring-2 focus:ring-gray-200 dark:text-gray-400 dark:hover:bg-gray-700 dark:focus:ring-gray-600" aria-controls="navbar-user" aria-expanded="false">
    <span class="sr-only">Open main menu</span>
    <svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 17 14">
        <path stroke="currentColor" stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M1 1h15M1 7h15M1 13h15"/>
    </svg>
</button>
""")


@readwrite_file(path=ROOT_SETTINGS_PATH)
def init_updates_to_settings_file(content: str) -> str:
    # Replace import statement for BASE_DIR
    content = content.replace(
        "from pathlib import Path",
        "from pathlib import Path\nimport os\nfrom dotenv import load_dotenv",
        1
    )

    # Add load_dotenv() under BASE_DIR
    content = content.replace(
        "BASE_DIR = Path(__file__).resolve().parent.parent",
        "BASE_DIR = Path(__file__).resolve().parent.parent\nload_dotenv()",
        1
    )

    # Replace DEBUG with os.getenv
    content = content.replace(
        "DEBUG = True",
        "DEBUG = os.getenv('DEBUG_MODE')",
        1
    )

    # Add root templates directory to TEMPLATES/DIRS
    new_template_dirs = '[\n'
    for item in TEMPLATES_DIRS_ADDITIONS:
        new_template_dirs += ''.join(f'\t\t\t{item}\n')
    new_template_dirs += '\t\t],'

    content = content.replace(
        "'DIRS': [],",
        f"'DIRS': {new_template_dirs}",
        1
    )
    return content


@readwrite_lines(path=ROOT_SETTINGS_PATH)
def update_secret_key(content: str, i: int, line: str) -> str:
    # Replace SECRET_KEY line with os.getenv
    if line.startswith("SECRET_KEY"):
        content[i] = "SECRET_KEY = os.getenv('DJANGO_SECRET_KEY')\n"
    return content


def generate_env_file() -> None:
    with open(".env", "w") as file:
        secret_key = subprocess.run(
            [os.path.join(VENV, "python"), "manage.py", "shell", "-c", "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"],
            capture_output=True, text=True
        ).stdout.strip()

        file.write(f"DJANGO_SECRET_KEY={secret_key}\n")
        file.write("DEBUG_MODE=True\n")
        file.write(f"DJANGO_SUPERUSER_PASSWORD={SUPERUSER_PASSWORD}")


@copy_files(file_or_dir='.gitignore')
def copy_gitignore(src_path: str, dest_path: str) -> None:
    shutil.copy(src_path, dest_path)


@copy_files(file_or_dir='imgs', middle_dest=ROOT_STATIC_FOLDER_URL)
def copy_imgs(src_path: str, dest_path: str) -> None:
    shutil.copytree(src_path, dest_path, dirs_exist_ok=True)


def update_installed_apps() -> None:
    installed_apps_str = __get_config_list_content("INSTALLED_APPS", "]", ROOT_SETTINGS_PATH)
    additions = ['\n\n    # 3rd party',  *INSTALLED_APPS_3RDPARTY, '\n    # local apps', *INSTALLED_APPS_LOCAL]
    __list_content_update(installed_apps_str, additions)


def update_middleware() -> None:
    middleware_str = __get_config_list_content("MIDDLEWARE", "]", ROOT_SETTINGS_PATH)
    additions = ['\n\n    # 3rd party',  *MIDDLEWARE_3RDPARTY_BOTTOM]
    __list_content_update(middleware_str, additions)


@readwrite_lines(path=ROOT_SETTINGS_PATH)
def add_staticfiles_config(content: str, i: int, line: str) -> str:
    if line.startswith("STATIC_URL"):
        static_url_line = f"STATIC_URL = '{STATIC_URL}'\n"
        static_root_line = f"STATIC_ROOT = os.path.join(BASE_DIR.parent, '{STATIC_ROOT_DIR}')\n\n"

        staticfiles_dir_str = "STATICFILES_DIRS = [\n"
        staticfiles_finders_str = "STATICFILES_FINDERS = [\n    # Default finders\n"

        for item in NEW_STATICFILES_DIRS:
            staticfiles_dir_str += ''.join(f'    {item}\n')
        staticfiles_dir_str += ']\n\n'

        for item in STATICFILES_DEFAULT_FINDERS:
            staticfiles_finders_str += ''.join(f'    {item}\n')
        staticfiles_finders_str += '\n    # 3rd party\n'

        for item in NEW_STATICFILES_3RDPARTY_FINDERS:
            staticfiles_finders_str += ''.join(f'    {item}\n')
        staticfiles_finders_str += ']\n\n'

        new_staticfile_settings = static_url_line + static_root_line + staticfiles_dir_str + staticfiles_finders_str
        content[i] = new_staticfile_settings
    return content


def add_compressor_config() -> None:
    with open(ROOT_SETTINGS_PATH, "a") as file:
        file.write("\n# Django compressor\n")
        file.write("# https://django-compressor.readthedocs.io/en/stable/\n\n")
        file.write(f"COMPRESS_ROOT = os.path.join(BASE_DIR, '{FIRSTAPP_DIR}', 'static')\n")
        file.write("COMPRESS_ENABLED = True\n")


@readwrite_file(path=ROOT_URLS_PATH)
def update_urlpatterns_root(content: str) -> str:
    content = content.replace(
        "from django.urls import path",
        "from django.urls import include, path\nfrom django.conf import settings",
        1
    )

    content = content.replace(
        "path('admin/', admin.site.urls),",
        "path('admin/', admin.site.urls),\n\tpath('__reload__/', include('django_browser_reload.urls')),\n\tpath('', include('core.urls')),",
        1
    )
    return content


def add_static_to_urlpatterns_root() -> None:
    with open(ROOT_URLS_PATH, "a") as file:
        file.write("\n\nif settings.DEBUG:\n")
        file.write("\tfrom django.conf.urls.static import static\n")
        file.write("\turlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)")


def update_urlpatterns_core() -> None:
    with open(FIRSTAPP_URLS_PATH, "a") as file:
        file.write("from django.urls import path, include\n")
        file.write("from . import views\n\n")
        file.write("urlpatterns = [\n")
        file.write("\tpath('', views.index, name='home'),\n")
        file.write("]")


def create_index_view_core() -> None:
    with open(FIRSTAPP_VIEWS_PATH, "a") as file:
        file.write("def index(request):\n")
        file.write("\treturn render(request, 'core/index.html')")


def migrate_db() -> None:
    subprocess.run([os.path.join(VENV, "python"), "manage.py", "makemigrations"])
    subprocess.run([os.path.join(VENV, "python"), "manage.py", "migrate"])


def create_superuser() -> None:
    subprocess.run([os.path.join(VENV, "python"), "manage.py", "createsuperuser", "--noinput", "--username", SUPERUSER_NAME, "--email", SUPERUSER_EMAIL])


def run_setup() -> None:
    # Step 2: Create a virtual environment
    print('Creating virtual environment...')
    create_virtual_environment()

    # Step 3: Access virtual environment, update pip, and install packages
    install_packages()

    # Step 4: Create requirements.txt
    create_requirements_txt()

    # Step 5: Run django-admin startproject
    run_django_startproject()

    # Step 6: Create static folder with css, js, imgs and template folder with base.html
    print('Creating static files and templates...', end='')
    make_static_dirs()
    copy_imgs()

    create_input_css()
    create_theme_toggle_script()
    create_core_template_base()
    create_core_template_index()
    create_core_navbar_component()
    print('Complete.')

    # Step 7: Add Tailwind CSS and Flowbite
    print("Installing Tailwind CSS...")
    add_tailwindcss()

    # Step 8: Add initial updates to config/settings.py
    print(f"Updating '{ROOT_SETTINGS_PATH}'...", end='')
    init_updates_to_settings_file()

    # Step 9: Update SECRET_KEY in config/settings.py
    update_secret_key()

    # Step 10: Generate .env file and duplicate .gitignore into project
    generate_env_file()
    copy_gitignore()

    # Step 11: Update INSTALLED_APPS in config/settings.py
    update_installed_apps()

    # Step 12: Update MIDDLEWARE in config/settings.py
    update_middleware()

    # Step 13: Add static files configuration to config/settings.py
    add_staticfiles_config()

    # Step 14: Add compressor configuration to config/settings.py
    add_compressor_config()

    # Step 15: Update config/urls.py and firstapp/urls.py
    print("Complete.")
    print(f"Updating '{ROOT_URLS_PATH}'...", end='')
    update_urlpatterns_root()
    add_static_to_urlpatterns_root()
    print("Complete.")

    print(f"Updating '{FIRSTAPP_DIR}'...", end='')
    create_index_view_core()
    update_urlpatterns_core()
    print("Complete.")

    # Step 16: Run initial database migration
    print("Migrating database...")
    migrate_db()
    create_superuser()

    # End of script
    print("Setup completed successfully.")


if __name__ == "__main__":
    root_directory_name = input("Enter the name of the root directory: ")

    # Handle existing project name
    if os.path.exists(root_directory_name):
        confirmation = input(f"A project already exists with that name ('{root_directory_name}')! Do you really want to delete it? (yes/no) ").lower()
    
        if confirmation == 'yes':
            try:
                if os.path.isdir(root_directory_name):
                    shutil.rmtree(root_directory_name)
                    print("Project successfully removed. Creating new one...")
                else:
                    print(f"The path '{root_directory_name}' is not a directory.")
                    sys.exit()
            except OSError as e:
                print(f'Error: {root_directory_name} -> {e}')
                sys.exit()
        else:
            print('Deletion cancelled.')
            sys.exit()


    # Step 1: Create a root directory
    create_root_directory(root_directory_name)
    
    # Run setup
    run_setup()
