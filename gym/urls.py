from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("api/sentence/", views.get_sentence, name="get_sentence"),
]
