
from django.conf import settings

from main.models.request import Request
from main.models.hard_drive import HardDrive
from datetime import datetime

def check_status():
    picked_up_hard_drives = HardDrive.objects.filter(status = HardDrive.Status.PICKED_UP)
    for hard_drive in picked_up_hard_drives:
        if datetime.now() > hard_drive.expected_hard_drive_return_date:
            hard_drive.request.status = Request.Request_Status.OVERDUE
            hard_drive.status = HardDrive.Status.OVERDUE
    
    print('checking status')
    
    

