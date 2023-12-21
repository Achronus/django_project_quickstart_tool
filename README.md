# Django Project Template
Welcome to the quick setup tool for creating a `Django` project with the following stack:

- [TailwindCSS](https://tailwindcss.com/) and [Flowbite](https://flowbite.com/)
- [AlpineJS](https://alpinejs.dev/)

- [Django HTMX](https://github.com/adamchainz/django-htmx)
- [Django Browser Reload](https://github.com/adamchainz/django-browser-reload) - for automatic page reloading during development

If you are fed up with the initial tedious process of setting up a new `Django` project, you've come to the right place! This tool eliminates all the boring minor changes needed to the `settings.py` file and runs the preliminary setup commands for activating a `Django` project, such as `projectstart`, `migrate`, and `createsuperuser`.

The tool does the following:
- Creates a virtual environment in the project folder
- Accesses it and installs the required packages
- Generates a `requirements.txt` file
- Creates a `.env` file with an updated `DJANGO_SECRET_KEY` ready for production using the `get_random_secret_key()` utility function
- Updates the `config/settings.py` file to include all the necessary required changes, such as:
  - Replacing values to access the `.env`
  - Updating `INSTALLED_APPS`
  - Updating `MIDDLEWARE`
  - Updating the `TEMPLATES DIRS`
  - Updating the `STATICFILES` section
  - Adding the `django-compressor` settings
- Creates a `firstapp`
- Updates `config/urls.py` to include `django-browser-reload` and `firstapp`
- Creates a `_base.html` and an `index.html` file in `core/templates`
- Creates a `Flowbite` navbar in `core/templates/components`
- Creates a `superuser` based on default values in the `setup.py` file
- Performs initial database `migration`

The default pip packages installed include:
- `django`
- `django-compressor`
- `django-browser-reload`
- `django-htmx`
- `python-dotenv`

_Note: all libraries and packages are automatically installed to their latest versions when running the tool._

# Customisation
The `setup.py` file has some customisation options at the top of the file under the section labelled `EDITABLE CONSTANTS`.

This includes the `createsuperuser` details.


# Dependencies
_Note: The install requires [NodeJS](https://nodejs.org/en), NPM, and [Python](https://www.python.org/downloads/) to be installed on your local machine._

1. To get started, clone the repository, enter the folder, run `setup.py`, and input a project name when prompted:
```bash
gh repo clone Achronus/django_project_quickstart_tool
cd django_project_quickstart_tool
python setup.py
```

That's it! Everything is setup with a blank template ready to start building a project from scratch.


Simply, run the `Django` server in a command line:
```bash
python manage.py runserver
```

And watch `Tailwind CSS` in another:
```
npm run dev
```


# Folder Structure
The folder structure should look similar to the following:
```bash
project_name
└── config
    └── __init__.py
    └── asgi.py
    └── settings.py
    └── urls.py
    └── wsgi.py
└── core
    └── migrations
        └── ...
    └── static
        └── imgs
            └── avatar.svg
        └── css
            └── input.css
            └── output.css
        └── js
            └── theme-toggle.js
    └── templates
        └── core
            └── components
                └── nav
                    └── mobile-nav.html
                └── navbar.html
            └── _base.html
            └── index.html
    └── __init__.py
    └── admin.py
    └── apps.py
    └── models.py
    └── tests.py
    └── urls.py
    └── views.py
└── node_modules
    └── ...
└── venv
    └── ...
└── .env
└── .gitignore
└── db.sqlite3
└── manage.py
└── package.json
└── package-lock.json
└── requirements.txt
└── tailwind.config.js
```

## Noteworthy Files and Folders
- `config/` - core settings created by using `django-admin startproject`
- `core/` - a standard app created using `python manage.py startapp` that stores the primary static files and templates for the project
- `core/templates/core/index.html` - application homepage