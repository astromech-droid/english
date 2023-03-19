from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("phrases/register", views.register_phrases, name="register_phrases"),
]
