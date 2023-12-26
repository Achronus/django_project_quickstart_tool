import os
import shutil
import subprocess
import sys
from functools import wraps
import urllib.request

from setup_assets.constants import *

project_name = ''  # Modified by user input


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


def __settings_content_update(old_content: str, additions: str) -> None:
    """Helper function for `update_installed_apps()` and `update_middleware()`. Updates a string of content given the `old_content` and a string of `additions`."""
    new_content = old_content + additions
    
    @readwrite_file(path=ROOT_SETTINGS_PATH)
    def update_content(content: str) -> str:
        return content.replace(
            old_content,
            new_content.strip(),
            1
        )

    update_content()


def __handle_project_name(project_name: str) -> str:
    """Helper function for replacing whitespace and dashes in the project name."""
    name_split = []

    if '-' in project_name:
        name_split = project_name.split('-')
    elif ' ' in project_name:
        name_split = project_name.split(' ')

    if len(name_split) != 0:
        project_name = '_'.join(name_split)
    
    return project_name.strip()


def __settings_formatter_loop(settings_items: list[str], additions: str) -> str:
    """Helper function to create an `additions` string for adding items to the `settings.py` file. Loops through the `settings_items` and adapts them to a specific format before adding them to `additions`."""
    for item in settings_items:
        additions += ''.join(f"    '{item}',\n")
    return additions


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


# Setup functions
def create_root_directory(directory_name: str) -> None:
    """Creates the root project directory."""
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


def move_setup_assets_to_project() -> None:
    """Duplicates the items in the `setup_assets` folder into the respective locations in the project directory."""
    try:
        # Move root folder assets into root project dir
        shutil.copytree(SETUP_ASSETS_ROOT_DIR, os.getcwd(), dirs_exist_ok=True)

        # Move static into firstapp static dir
        shutil.copytree(SETUP_ASSETS_STATIC_DIR, ROOT_STATIC_FOLDER_URL, dirs_exist_ok=True)

        # Move templates into firstapp templates dir
        shutil.copytree(SETUP_ASSETS_TEMPLATE_DIR, ROOT_TEMPLATE_FOLDER_URL, dirs_exist_ok=True)

        # Update firstapp folder name
        setup_firstapp_dir_name = os.path.join(ROOT_TEMPLATE_FOLDER_URL, SETUP_FIRSTAPP_DIR)
        new_firstapp_dir_name = os.path.join(os.path.dirname(setup_firstapp_dir_name), FIRSTAPP_DIR)

        os.rename(setup_firstapp_dir_name, new_firstapp_dir_name)
    except FileNotFoundError as e:
        raise FileNotFoundError(f"{e}\nDoes a 'setup_assets' folder exist in: '{os.getcwd()}' and contain the required folder?")


def configure_npm_assets() -> None:
    subprocess.run(["npm", "install", "-D", "tailwindcss"], shell=True)
    subprocess.run(["npm", "install", "flowbite", "alpinejs"], shell=True)
    
    subprocess.run(["npx", "tailwindcss", "-i", f"./{FIRSTAPP_DIR}/static/css/input.css", "-o", f"./{FIRSTAPP_DIR}/static/css/output.css"], shell=True)

    # Update package.json for watching tailwindcss with 'dev' command
    @readwrite_file(path=os.path.join(os.getcwd(), "package.json"))
    def update_content(content: str) -> str:
        old_content = '"devDependencies": {'
        tw_css_cmd = f"npx tailwindcss -i ./{FIRSTAPP_DIR}/static/css/input.css -o ./{FIRSTAPP_DIR}/static/css/output.css --watch"
        new_content = '"scripts": {\n\t\t"dev": ' + f'"{tw_css_cmd}"' + '\n\t},\n\t' + old_content

        content = content.replace(
            old_content,
            new_content,
            1
        )
        return content
    
    update_content()


def download_js_libraries_to_static() -> None:
    # Copy Flowbite from node_modules
    shutil.copy(FLOWBITE_URL, os.path.join(ROOT_STATIC_FOLDER_URL, 'js', FLOWBITE_FILENAME))

    # Retrieve HTMX from official downloads page
    with urllib.request.urlopen(HTMX_URL) as response:
        htmx_content = response.read().decode('utf-8')
    
    with open(os.path.join(ROOT_STATIC_FOLDER_URL, 'js', HTMX_FILENAME), 'w') as file:
        file.write(htmx_content)

    # Retrieve AlpineJS from node_modules
    shutil.copy(ALPINE_URL, os.path.join(ROOT_STATIC_FOLDER_URL, 'js', ALPINE_FILENAME))


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
        new_template_dirs += ''.join(f'\t\t\t{item},\n')
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

    # Add additional custom config settings
    with open(".env", "a") as file:
        for item in ENV_FILE_ADDITIONAL_PARAMS:
            file.write(item)


def update_installed_apps() -> None:
    installed_apps_str = __get_config_list_content("INSTALLED_APPS", "]", ROOT_SETTINGS_PATH)

    additions = '\n\n    # 3rd party\n'
    additions = __settings_formatter_loop(INSTALLED_APPS_3RDPARTY, additions)

    additions += '\n    # local apps\n' 
    additions = __settings_formatter_loop(INSTALLED_APPS_LOCAL, additions)

    __settings_content_update(installed_apps_str, additions)


def update_middleware() -> None:
    middleware_str = "'django.contrib.sessions.middleware.SessionMiddleware',"

    additions = '\n\n    # 3rd party\n'
    additions = __settings_formatter_loop(MIDDLEWARE_3RDPARTY, additions)
    additions += "\n    # Core\n"

    __settings_content_update(middleware_str, additions)


@readwrite_lines(path=ROOT_SETTINGS_PATH)
def add_staticfiles_config(content: str, i: int, line: str) -> str:
    if line.startswith("STATIC_URL"):
        static_url_line = f"STATIC_URL = '{STATIC_URL}'\n"
        static_root_line = f"STATIC_ROOT = os.path.join(BASE_DIR.parent, '{STATIC_ROOT_DIR}')\n\n"

        staticfiles_dir_str = "STATICFILES_DIRS = [\n]\n\n"
        staticfiles_finders_str = "STATICFILES_FINDERS = [\n    # Default finders\n"

        staticfiles_finders_str = __settings_formatter_loop(STATICFILES_DEFAULT_FINDERS, staticfiles_finders_str)
        staticfiles_finders_str += '\n    # 3rd party\n'

        staticfiles_finders_str = __settings_formatter_loop(NEW_STATICFILES_3RDPARTY_FINDERS, staticfiles_finders_str)
        staticfiles_finders_str += ']\n\n'

        new_staticfile_settings = static_url_line + static_root_line + staticfiles_dir_str + staticfiles_finders_str
        content[i] = new_staticfile_settings
    return content


@readwrite_file(path=ROOT_SETTINGS_PATH)
def update_staticfiles_dirs(content: str) -> str:
    staticfiles_dir_str = 'STATICFILES_DIRS = ['
    for item in NEW_STATICFILES_DIRS:
        staticfiles_dir_str += ''.join(f'\n   {item},')

    content = content.replace(
        "STATICFILES_DIRS = [",
        staticfiles_dir_str,
        1
    )
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
        f"path('admin/', admin.site.urls),\n\tpath('__reload__/', include('django_browser_reload.urls')),\n\tpath('', include('{FIRSTAPP_DIR}.urls')),",
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
        file.write(f"\treturn render(request, '{FIRSTAPP_DIR}/index.html')")


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

    # Step 6: Moving root, static, and template setup assets to project
    print('Creating static files and templates...', end='')
    move_setup_assets_to_project()
    print('Complete.')

    # Step 7: Add initial updates to config/settings.py
    print(f"Updating '{ROOT_SETTINGS_PATH}'...", end='')
    init_updates_to_settings_file()

    # Step 9: Update SECRET_KEY in config/settings.py
    update_secret_key()

    # Step 10: Generate .env file
    generate_env_file()

    # Step 11: Update INSTALLED_APPS in config/settings.py
    update_installed_apps()

    # Step 12: Update MIDDLEWARE in config/settings.py
    update_middleware()

    # Step 13: Add static files configuration to config/settings.py
    add_staticfiles_config()
    update_staticfiles_dirs()

    # Step 14: Add compressor configuration to config/settings.py
    add_compressor_config()
    print("Complete.")

    # Step 15: Add Tailwind CSS and Flowbite
    print("Installing Tailwind CSS...")
    configure_npm_assets()

    # Step 16: Add HTMX, AlpineJS, and Flowbite to static folder
    print("Downloading HTMX, AlpineJS, and Flowbite...", end='')
    download_js_libraries_to_static()
    print("Complete.")

    # Step 17: Update config/urls.py and firstapp/urls.py
    print(f"Updating '{ROOT_URLS_PATH}'...", end='')
    update_urlpatterns_root()
    add_static_to_urlpatterns_root()
    print("Complete.")

    print(f"Updating '{FIRSTAPP_DIR}'...", end='')
    create_index_view_core()
    update_urlpatterns_core()
    print("Complete.")

    # Step 18: Run initial database migration
    print("Migrating database...")
    migrate_db()
    create_superuser()

    # End of script
    print("Setup completed successfully.")


if __name__ == "__main__":
    print("Note: we automatically replace 'whitespaces' and '-' with '_'.")
    project_name = input("Enter the name of the root directory: ")
    project_name = __handle_project_name(project_name)
    print(f"Project name set to: '{project_name}'")

    # Handle existing project name
    if os.path.exists(project_name):
        confirmation = input(f"A project already exists with that name ('{project_name}')! Do you really want to delete it? (yes/no) ").lower()
    
        if confirmation == 'yes':
            try:
                if os.path.isdir(project_name):
                    shutil.rmtree(project_name)
                    print("Project successfully removed. Creating new one...")
                else:
                    print(f"The path '{project_name}' is not a directory.")
                    sys.exit()
            except Exception as e:
                print(f'Error: {os.path.join(os.getcwd(), project_name)} -> {e}')
                sys.exit()
        else:
            print('Deletion cancelled.')
            sys.exit()


    # Step 1: Create a root directory
    create_root_directory(project_name)
    
    # Run setup
    run_setup()
