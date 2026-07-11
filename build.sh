#!/usr/bin/env bash
# exit on error
set -o errexit

pip install -r requirements.txt

# Run migrations and collect static files
# We use 'mysite/manage.py' because the project is in a subdirectory
mkdir -p mysite/media/images
python mysite/manage.py collectstatic --no-input
python mysite/manage.py migrate

# Create superuser if environment variables are present
if [[ $DJANGO_SUPERUSER_USERNAME ]]; then
  echo "Setting up superuser..."
  python mysite/manage.py shell -c "from django.contrib.auth.models import User; import os; username = os.environ.get('DJANGO_SUPERUSER_USERNAME'); email = os.environ.get('DJANGO_SUPERUSER_EMAIL'); password = os.environ.get('DJANGO_SUPERUSER_PASSWORD'); User.objects.filter(username=username).exists() or User.objects.create_superuser(username, email, password)" || true
fi
