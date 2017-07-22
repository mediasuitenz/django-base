# Django Base
A starting point for a Media Suite Django project.

Aims to get you up and running with a working instance that will run in both
Docker and using the Django development server.

## Installing project

For the following steps replace <project_name> with your project name.

NOTE: Assumes virtualenv is setup and commands are run from the same dir as this
README.

### 1. Create Virtualenv and install dependencies

```
# Create virtual environment and activates it
mkvirtualenv <project_name>

# Install Django and some deps
pip install -r server/requirements.txt

# Locks the software versions to the installed versions
pip freeze > server/requirements.txt
```

### 2. Create Django Project

```
django-admin startproject <project_name> server/
```

### 3. Update settings

Edit `server/<project_name>/settings.py`.

Change
`SECRET_KEY = 'ybf-y*axmeeu*...'`
to
`SECRET_KEY = os.environ.get('SECRET_KEY')`.

Change
`DEBUG = True`
to
`DEBUG = str(os.environ.get('DEBUG')).lower() in ['true', '1']`.

Add to end of file
`STATIC_ROOT = os.path.join(BASE_DIR, '..', 'static')`.

### 4. Update deployment files

Edit `docker-config/uwsgi.ini` and change `<project_name>` in the module setting to the
name of the project created above by `django-admin`.

### 5. Setup .env file

Copy `.env-example` to `.env` and run `scripts/keygen.py` to generate a value
for the `SECRET_KEY` setting.

Update `server/manage.py` and add the following block near the top:
```
from os.path import join, dirname, isfile
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '..', '.env')
if os.path.isfile(dotenv_path):
    load_dotenv(dotenv_path)
```

### 6. Final steps

Delete the `.git` directory to disconnect from the `base-django` repo, and
import the code into your new repo.

## Development server

At this point you should be able to run the development server
`python server/manage.py runserver` and browse to http://localhost:8000/.

## Docker build

Uses Ubuntu 16.04 as the base for the deployed image and will use the versions
provided for Python, Nginx, and Supervisor.

To build run `docker build --tag=<image_name> .`.

To run a container `docker run -d --env-file=.env -p <local_port>:80 <image_name>`.

Test by browsing to http://localhost:<local_port>/.

### Ensuring local version of Python matches

You should make sure your local Python version matches the deployed version. Run
this command to find what version the container has
`docker run --rm <image_name> python3 -V`.
