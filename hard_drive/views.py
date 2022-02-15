from django.shortcuts import render
from django.http import HttpResponse

# Dummy data of hard Drive
hard_drive = {
    "id":"",
    "status":"On",
    "serial_numbers":"",
    "classification":"classified",
    "image_version":"image_1",
    "date_of_last_boot_test":123141241,#timestamp
    "boot_test_status":"",
    "connection_port":"",
    "issue_date":19234352, #timestamp
    "text_comment":"",
    "request_id":""
}


# Create your views here.

def drive_view(request):
    return HttpResponse('Our First Drive Yay!!')
