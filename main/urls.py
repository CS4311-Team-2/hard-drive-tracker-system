from django.urls import path
from .import views

app_name = 'main'

urlpatterns = [
    path('', views.index, name='index'),  
    path('all_listings/', views.all_listings, name='all_listings'),
    path('new_listing/', views.new_listing, name='new_listing'),
    path('all_listings/<detail_id>/', views.detail, name='detail'),
    path('edit_listings/<edit_id>/', views.edit_listing, name='edit_listing')

]