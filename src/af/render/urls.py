from render import dash_app
from django.urls import path

from .views import plots

urlpatterns = [
    path("t/", plots),
]
