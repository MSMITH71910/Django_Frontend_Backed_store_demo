import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from allauth.socialaccount.models import SocialApp
try:
    print(SocialApp.sites)
except Exception as e:
    print(f"Error accessing sites: {e}")
