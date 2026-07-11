#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Run migrations and collect static files
# We use 'mysite/manage.py' because the project is in a subdirectory
python mysite/manage.py collectstatic --no-input
python mysite/manage.py migrate
