import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'mysite.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

def fix():
    # Use site 1 or whatever site exists
    site = Site.objects.filter(domain='127.0.0.1:8000').first()
    if not site:
        site = Site.objects.first()
        if site:
            site.domain = '127.0.0.1:8000'
            site.name = '127.0.0.1:8000'
            site.save()
        else:
            site = Site.objects.create(domain='127.0.0.1:8000', name='127.0.0.1:8000')
    
    print(f"Using Site: {site.domain} (ID: {site.id})")

    app, created = SocialApp.objects.get_or_create(
        provider='google',
        name='Google Auth'
    )
    app.client_id = 'place-your-client-id-here'
    app.secret = 'place-your-client-secret-here'
    app.save()
    app.sites.add(site)
    
    print(f"Configured Google SocialApp for site {site.id}")

if __name__ == "__main__":
    fix()
