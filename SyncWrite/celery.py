#!/usr/bin/env python3

"""Celery configuration"""

from __future__ import absolute_import, unicode_literals
import os
from celery import Celery

# os.environ['DJANGO_SETTINGS_MODULE'] = os.getenv('DJANGO_SETTINGS_MODULE', 'RentEase.settings.dev')
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SyncWrite.settings.dev')


# Create a Celery instance
app = Celery('SyncWrite')

# Load the Django settings for Celery
app.config_from_object('django.conf:settings', namespace='CELERY')
# Auto-discover tasks
app.autodiscover_tasks(['sync.utils'])

# Set Celery log level to debug
app.conf.update(
    task_track_started=True,  # Track the started state of tasks (optional)
    loglevel='DEBUG',         # Set log level to debug
)

app.conf.broker_connection_max_retry_on_startup = True

if __name__ == '__main__':
    app.start()
