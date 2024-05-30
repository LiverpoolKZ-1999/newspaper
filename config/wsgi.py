from os import environ

from django.core.handlers.wsgi import WSGIHandler
from django.core.wsgi import get_wsgi_application
from whitenoise import WhiteNoise

environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")
wsgi_application: WSGIHandler = get_wsgi_application()
application = WhiteNoise(
    application=wsgi_application,
    root="/app/static",
)
