from django.core.management.base import BaseCommand
from django.contrib.auth.models import User, Group

from main.models.event import Event
from main.models.hard_drive_request import HardDriveRequest
from main.models.request import Request
from main.models.hard_drive import HardDrive
from main.models.configurations.hard_drive_type import HardDriveType
from main.models.configurations.hard_drive_connection_ports import HardDriveConnectionPorts
from main.models.configurations.hard_drive_manufacturers import HardDriveManufacturers
from users.models import UserProfile

import pandas as pd


ADMIN_USERNAME = 'Admin'
MAINTAINER_USERNAME = 'Maintainer'
REQUESTOR_USERNAME = 'Requestor'
PASSWORD = 'pass'

class Command(BaseCommand):
    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        
        if not UserProfile.objects.filter(username__iexact=ADMIN_USERNAME).exists():
            user = UserProfile.objects.create_superuser(username=ADMIN_USERNAME,
                                 email='admin@army.mil')
            user.set_password(PASSWORD)
            user.status = UserProfile.Status.ACTIVE
            user.save()

        maintainer_gp, _ = Group.objects.update_or_create(name='Maintainer')
        maintainer_gp.save()

        requester_gp, _ = Group.objects.update_or_create(name='Requestor')
        requester_gp.save()

        if not UserProfile.objects.filter(username__iexact=MAINTAINER_USERNAME).exists():
            user = UserProfile.objects.create(username=MAINTAINER_USERNAME,
                                 email='maintainer@army.mil')
            user.set_password(PASSWORD)
            user.status = UserProfile.Status.ACTIVE
       
            maintainer_gp.user_set.add(user)
            user.save()

        if not UserProfile.objects.filter(username__iexact=REQUESTOR_USERNAME).exists():
            user = UserProfile.objects.create(username=REQUESTOR_USERNAME,
                                 email='requestor@army.mil')
            user.set_password(PASSWORD)
            user.status = UserProfile.Status.ACTIVE

            requester_gp.user_set.add(user)
            user.save()
        
        df = pd.read_csv('request.csv')
        for (request_reference_no, request_reference_no_year, request_status, request_creation_date,
             request_last_modified_date, need_drive_by_date, comment) \
        in zip(df.request_reference_no, df.request_reference_no_year, df.request_status, df.request_creation_date,
            df.request_last_modified_date, df.need_drive_by_date, df.comment):

            request = Request(request_reference_no, request_reference_no_year, request_status, request_creation_date,
                request_last_modified_date, need_drive_by_date, comment)

            request.save()
    
        df = pd.read_csv('event.csv')
        for (id, event_name, event_description, event_location, event_type, length_of_reporting_cycles,
            event_status, event_start_date, event_end_date) \
        in zip(df.id, df.event_name, df.event_description, df.event_location, df.event_type, df.length_of_reporting_cycles,
            df.event_status, df.event_start_date, df.event_end_date):

            event = Event(id, event_name, event_description, event_location, event_type, length_of_reporting_cycles,
                event_status, event_start_date, event_end_date)

            request = Request.objects.get(pk = 1)            
            event.request = request
            event.save()

        df = pd.read_csv('hard_drives.csv')
        for (id, create_date, serial_number, manufacturer,
            model_number, hard_drive_type, connection_port,
            hard_drive_size, classification, justification_for_classification_change,
            hard_drive_image, imange_version_id, boot_test_status, boot_test_expiration, status, 
            justification_for_hard_drive_status_change, issue_date, expected_hard_drive_return_date,
            justification_for_hard_drive_return_date, actual_return_date, modified_date) \
        in zip(df.id, df.create_date, df.serial_number, df.manufacturer, df.model_number, 
            df.hard_drive_type, df.connection_port, df.hard_drive_size, df.classification, 
            df.justification_for_classification_change, df.hard_drive_image, df.imange_version_id, df.boot_test_status, 
            df.boot_test_expiration, df.status, df.justification_for_hard_drive_status_change, 
            df.issue_date, df.expected_hard_drive_return_date, df.justification_for_hard_drive_return_date, 
            df.actual_return_date, df.modified_date):

            models = HardDrive(id, create_date, serial_number, manufacturer, 
            model_number, hard_drive_type, connection_port, hard_drive_size, classification, 
            justification_for_classification_change, hard_drive_image, imange_version_id, boot_test_status, boot_test_expiration, 
            status, justification_for_hard_drive_status_change, issue_date, expected_hard_drive_return_date, 
            justification_for_hard_drive_return_date, actual_return_date, modified_date)

            models.save()

        df = pd.read_csv('hard_drive_requests.csv')
        for (id,classification,amount_required,connection_port,hard_drive_size,hard_drive_type,comment) \
        in zip(df.id,df.classification,df.amount_required,df.connection_port,df.hard_drive_size,df.hard_drive_type,df.comment):
            models = HardDriveRequest(id,classification,amount_required,connection_port,hard_drive_size,hard_drive_type,comment)
            request = Request.objects.get(pk = 1)
            
            models.request = request
            models.save()
        
        requestor = UserProfile.objects.get(username__iexact = REQUESTOR_USERNAME)
        requests = Request.objects.all()
        for request in requests:
            request.user = requestor
            request.save()

        hard_drives = HardDrive.objects.all()[:3]
        for hard_drive in hard_drives:
            # Overdue Request
            hard_drive.request = requests[3]
            hard_drive.save()
        
        # Configurations
        HardDriveManufacturers.objects.create(name="HP")
        HardDriveManufacturers.objects.create(name="Samsung")
        HardDriveConnectionPorts.objects.create(name="SATA")
        HardDriveConnectionPorts.objects.create(name="USB")
        HardDriveType.objects.create(name="SSD")
        HardDriveType.objects.create(name="HDD")
        HardDriveType.objects.create(name="NVMe")

        print('Succesfully added dummy data')
        