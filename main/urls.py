
from django.urls import path
from main.views import maintainer, requestor, views


app_name = 'main'

urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),

    path('', views.index, name='index'), 
    path('view_request/', views.view_request, name='view_request'),
    path('make_request/', views.make_request, name='make_request'),
    path('add_hard_drive/', views.add_hard_drive, name = 'add_hard_drive'),

    path('request/put/<int:id>', requestor.update_request, name = 'update_request'),
]