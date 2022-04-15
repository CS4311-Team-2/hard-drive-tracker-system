
from urllib import request
from django.conf import settings

from main.models.request import Request
from main.models.hard_drive import HardDrive
from datetime import date

def check_status():
    #Check for hard drive constrains
    picked_up_hard_drives = HardDrive.objects.filter(status = HardDrive.Status.PICKED_UP)
    for hard_drive in picked_up_hard_drives:
        if date.today() > hard_drive.expected_hard_drive_return_date:
            hard_drive.request.request_status = Request.Request_Status.OVERDUE
            hard_drive.request.save()

            hard_drive.status = HardDrive.Status.OVERDUE
            hard_drive.save()

    
    #Check for request constrains
    requests = Request.objects.all()
    for request in requests:
        hard_drives = HardDrive.objects.filter(request = request)
        for hard_drive in hard_drives:
            if hard_drive.status == HardDrive.Status.OVERDUE:
                request.request_status = Request.Request_Status.OVERDUE
                request.save()

    print('checking status')
    
    

