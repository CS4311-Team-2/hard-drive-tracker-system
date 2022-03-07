
from django.urls import path
from .views import views

app_name = 'main'

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

<<<<<<< HEAD
    path('', views.index, name='index'),  
    path('all_listings/', views.all_listings, name='all_listings'),
    path('new_listing/', views.new_listing, name='new_listing'),
    path('maintainer/', views.maintainer_home, name='maintainer_home'),
    path('requestor/make_requestor', views.requestor_makes_request, name='requestor_makes_request'),
=======
    path('', views.index, name='index'), 
    path('view_request/', views.view_request, name='view_request'),
    path('make_request/', views.make_request, name='make_request'),
    path('add_hard_drive/', views.add_drive, name = 'add_hard_drive'),
>>>>>>> origin/main
]