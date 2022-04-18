
from django.urls import path
from main.views import maintainer, requestor, views, htmx, administrator


app_name = 'main'

# Implemented inferfaces
urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logoutUser, name='logout'),
    path('', views.index, name='index'), 
    path('view_request/<int:key_id>', views.view_request, name='view_request'),
    path('view_all_requests/', views.view_all_requests, name='view_all_requests'),
    path('make_request/', views.make_request, name='make_request'),
    path('edit_request/<int:key_id>', views.edit_request, name='edit_request'),
    
    path('add_hard_drive/', views.add_hard_drive, name = 'add_hard_drive'),
    path('view_hard_drive/<int:id>/', views.view_hard_drive, name="view_hard_drive"),
    path('view_all_harddrives/', views.view_all_harddrives, name='view_all_harddrives'),
    path('view_all_profiles/', views.view_all_profiles, name="view_all_profiles"),
    

    path('view_user_profile/<int:id>', maintainer.view_user_profile, name="view_user_profile"),
    path('view_profile/', views.view_profile, name="view_profile"),
    path('create_user_profile/', views.create_user_profile, name="create_user_profile"),

    path('request/<int:id>', requestor.view_single_request, name = 'update_request'),
    path('hard_drive_request/create', requestor.add_hard_drive_request, name = 'create_hd_request'),
    path('log/', maintainer.view_log, name='log'),
    path('configuration/', views.configuration, name="configuration"),

    # Htmx configurations
    path('hard_drive_types/', htmx.hard_drive_type, name = "hard_drive_type"), 
    path('delete-hard-drive-type/<int:pk>/', htmx.delete_hard_drive_type, name="delete-hard-drive-type"), 

    path('hard_drive_manufacturers/', htmx.hard_drive_manufacturer, name="hard_drive_manufacturers"),
    path('delete-hard-drive-manufacturers/<int:pk>/', htmx.delete_hard_drive_manufacturer, name="delete-hard-drive-manufacturers"),

    path('hard_drive_connection_port/', htmx.hard_drive_connection_port, name="hard_drive_connection_port"),
    path('delete-hard-drive-connection-port/<int:pk>/', htmx.delete_hard_drive_connection_port, name="delete-hard-drive-connection-port"),

    path('hard_drive_size/', htmx.hard_drive_size, name="hard_drive_size"),
    path('delete-hard-drive-size/<int:pk>/', htmx.delete_hard_drive_size, name="delete-hard-drive-size"),

    path('assign_hard_drive/', htmx.assign_hard_drive, name="assign_hard_drive"),
    path('approve_request/', htmx.approve_request, name="approve_request"),

    #TODO: We can prolly just reuse the maintainer homepage
    path('auditor/', views.auditor.home, name='home'),    
]