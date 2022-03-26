
from django.urls import path
from main.views import maintainer, requestor, views


app_name = 'main'

# Implemented inferfaces
urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.index, name='index'), 
    path('view_request/', views.view_request, name='view_request'),
    path('view_all_requests/', views.view_all_requests, name='view_all_requests'),
    path('make_request/', views.make_request, name='make_request'),
    path('add_hard_drive/', views.add_hard_drive, name = 'add_hard_drive'),
    path('view_all_harddrives/', views.view_all_harddrives, name='view_all_harddrives'),

    path('request/<int:id>', requestor.view_single_request, name = 'update_request'),
    path('hard_drive_request/create', requestor.add_hard_drive_request, name = 'create_hd_request'),

    path('configuration/', views.configuration, name="configuration"),
]