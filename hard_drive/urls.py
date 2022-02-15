from django.urls import path
from .views import add_drive_view, drive_view

urlpatterns = [
    path('', drive_view),
    path('add/', add_drive_view),
]
