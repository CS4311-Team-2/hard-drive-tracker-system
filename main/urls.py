
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
    path('maintainer/', views.maintainer_home, name='maintainer_home'),
    path('maintainer/request', views.maintainer_view_all_requests, name='maintainer_view_all_requests')
]