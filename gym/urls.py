from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("train", views.train, name="train"),
    path("phrases", views.list_phrases, name="list_phrases"),
    path("logs", views.list_logs, name="list_logs"),
    path("phrases/register", views.html_register_phrases, name="html_register_phrases"),
    path("api/phrases/register", views.api_register_phrases, name="api_register_phrases"),
    path("api/phrases/logging", views.api_logging, name="api_logging"),
]
