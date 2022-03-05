from lib2to3.pytree import Base
from django.core.management.base import BaseCommand
import pandas as pd
from main.models.event import Event
from main.models.request import Request
from main.models.hard_drive import HardDrive
from django.contrib.auth.models import User, Group



MAINTAINER_USERNAME = 'Maintainer'
REQUESTOR_USERNAME = 'Requestor'
PASSWORD = 'Pass123!'

class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        df = pd.read_csv('request.csv')
        for (id, request_reference_no, request_reference_no_year, request_status, request_creation_date,
             request_last_modified_date, need_drive_by_date, comment) \
        in zip(df.id, df.request_reference_no, df.request_reference_no_year, df.request_status, df.request_creation_date,
             df.request_last_modified_date, df.need_drive_by_date, df.comment):

            models = Request(id, request_reference_no, request_reference_no_year, request_status, request_creation_date,
             request_last_modified_date, need_drive_by_date, comment)

            models.save()
    
        df = pd.read_csv('event.csv')
        for (id, event_name, event_description, event_location, event_type, length_of_reporting_cycles,
         event_status, event_start_date, event_end_date) \
        in zip(df.id, df.event_name, df.event_description, df.event_location, df.event_type, df.length_of_reporting_cycles,
         df.event_status, df.event_start_date, df.event_end_date):

            models = Event(id, event_name, event_description, event_location, event_type, length_of_reporting_cycles,
         event_status, event_start_date, event_end_date)

            models.save()

        df = pd.read_csv('hard_drives.csv')
        for (id, create_date, serial_number, manufacturer,
            model_number, hard_drive_type, connection_port,
            hard_drive_size, classification, justification_for_classification_change,
            imange_version_id, boot_test_status, boot_test_expiration, status, 
            justification_for_hard_drive_status_change, issue_date, expected_hard_drive_return_date,
            justification_for_hard_drive_return_date_status_change, actual_return_date, modified_date) \
        in zip(df.id, df.create_date, df.serial_number, df.manufacturer, df.model_number, 
            df.hard_drive_type, df.connection_port, df.hard_drive_size, df.classification, 
            df.justification_for_classification_change, df.imange_version_id, df.boot_test_status, 
            df.boot_test_expiration, df.status, df.justification_for_hard_drive_status_change, 
            df.issue_date, df.expected_hard_drive_return_date, df.justification_for_hard_drive_return_date_status_change, 
            df.actual_return_date, df.modified_date):

            models = HardDrive(id, create_date, serial_number, manufacturer, 
            model_number, hard_drive_type, connection_port, hard_drive_size, classification, 
            justification_for_classification_change, imange_version_id, boot_test_status, boot_test_expiration, 
            status, justification_for_hard_drive_status_change, issue_date, expected_hard_drive_return_date, 
            justification_for_hard_drive_return_date_status_change, actual_return_date, modified_date)

            models.save()

        maintainer_gp, _ = Group.objects.update_or_create(name='Maintainer')
        maintainer_gp.save()

        requester_gp, _ = Group.objects.update_or_create(name='Requestor')
        requester_gp.save()

        if not User.objects.filter(username__iexact=MAINTAINER_USERNAME).exists():
            user, _ = User.objects.update_or_create(username=MAINTAINER_USERNAME,
                                 email='maintainer@gmail.com',
                                 password=PASSWORD)

            maintainer_gp.user_set.add(user)
            user.save()

        if not User.objects.filter(username__iexact=REQUESTOR_USERNAME).exists():
            user, _ = User.objects.update_or_create(username=REQUESTOR_USERNAME,
                                 email='requestor@gmail.com',
                                 password=PASSWORD)
            
            requester_gp.user_set.add(user)
            user.save()

        