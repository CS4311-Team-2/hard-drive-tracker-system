from django.shortcuts import render
from django.http import HttpResponse

# Dummy data of hard Drive
# All fields are taken from the SRS
hard_drive = {
    "id":"",
    "create_date": 123124321, #timestamp
    "manufacturer": "", 
    "model_number":"",
    "hard_drive_type":"",
    "connection_port":"",
    "hard_drive_size":"", 
    "status":"Assigned", #{Available, Assigned, End-of-life, etc}
    "serial_number":"",
    "classification":"classified",
    "image_version_id": 1234,
    "boot_test_expiration":123141241,#timestamp
    "boot_test_status":"",
    "justification_for_hard_drive_status_change":"",
    "connection_port":"",
    "issue_date":19234352, #timestamp
    "request_id":"" # Foreign Key to request
}


# Create your views here.

def drive_view(request):
    return HttpResponse('Our First Drive Yay!!')
