import os

from celery import Celery

celery_handler = Celery("af")


def init_producer():
    """Initilise the producer for the app"""
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
    celery_handler.config_from_object("django.conf:settings", namespace="CELERY")
    celery_handler.autodiscover_tasks()


init_producer()
