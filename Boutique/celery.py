# from __future__ import absolute_import

# import os
# from celery import Celery
# # from tufleur.settings import base as settings
# from django.conf import settings

# # set Django settings module for celery program.
# os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')

# app = Celery('hello_django')

# # Using a string here means the worker will not have to
# # pickle the object when using Windows.
# app.config_from_object('config.settings')
# app.autodiscover_tasks(lambda: settings.INSTALLED_APPS)

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# set the default Django settings module for the 'celery' program.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Boutique.settings')

app = Celery('Boutique')

# Using a string here means the worker don't have to serialize
# the configuration object to child processes.
# - namespace='CELERY' means all celery-related configuration keys
#   should have a `CELERY_` prefix.
app.config_from_object('django.conf:settings', namespace='CELERY')

# Load task modules from all registered Django app configs.
app.autodiscover_tasks()

@app.task(bind=True)
def debug_task(self):
  print('Request: {0!r}'.format(self.request))