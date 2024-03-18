from django.urls import path
from .views import trigger, result, is_alive


urlpatterns = [
    path("trigger", trigger),
    path("result/<str:job_id>", result),
    path("is-alive", is_alive),
    path("result", result),
]
