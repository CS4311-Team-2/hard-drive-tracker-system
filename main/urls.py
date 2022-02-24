<<<<<<< HEAD
from unicodedata import name
=======

>>>>>>> main
from django.urls import path
from . import views

app_name = 'main'

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.index, name='index'),  
    path('all_listings/', views.all_listings, name='all_listings'),
    path('new_listing/', views.new_listing, name='new_listing'),
<<<<<<< HEAD
    path('all_listings/<detail_id>/', views.detail, name='detail'),
    path('edit_listings/<edit_id>/', views.edit_listing, name='edit_listing')
<<<<<<< HEAD
=======

>>>>>>> ec1e4124f3ef65649691a3d8d3d91e1a8997c6f5
=======
    path('maintainer/hard_drives/', views.maintainer_home)
>>>>>>> main
]