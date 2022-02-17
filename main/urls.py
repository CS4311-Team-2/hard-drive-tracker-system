from django.urls import path
from .import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),  
    path('all_listings/', views.all_listings, name='all_listings'),
    path('new_listing/', views.new_listing, name='new_listing')
]