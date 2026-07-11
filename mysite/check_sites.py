import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from allauth import app_settings
print(f"SITES_ENABLED: {app_settings.SITES_ENABLED}")
