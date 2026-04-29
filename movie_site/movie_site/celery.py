import os
from celery import celery

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'movie_site.settings')

app = Celery('movie_site')
app.config_from_object('django.conf:settings', namespace = 'CELERY')
app.autodiscover_tasks()

