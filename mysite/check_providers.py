import os
import django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()
from allauth.socialaccount.adapter import get_adapter
adapter = get_adapter()
try:
    app = adapter.get_app(None, 'google')
    print(f"App: {app.provider}, ID: {app.client_id}")
except Exception as e:
    print(f"Error: {e}")
