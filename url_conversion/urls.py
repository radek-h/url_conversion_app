from django.urls import path

from .views import convert_url

urlpatterns = [
    path("convert/", convert_url, name="convert-url"),
]
