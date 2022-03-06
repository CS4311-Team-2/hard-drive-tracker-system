from lib2to3.pytree import Base
from django.core.management.base import BaseCommand
import pandas as pd
from main.models.hard_drive import HardDrive
from django.contrib.auth.models import User, Group
from django.contrib.auth import authenticate

MAINTAINER_USERNAME = 'Maintainer'
REQUESTOR_USERNAME = 'Requestor'
PASSWORD = 'pass'

class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
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

        maintainer_gp, _ = Group.objects.update_or_create(name='Maintainer')
        maintainer_gp.save()

        requester_gp, _ = Group.objects.update_or_create(name='Requestor')
        requester_gp.save()

        if not User.objects.filter(username__iexact=MAINTAINER_USERNAME).exists():
            user = User.objects.create(username=MAINTAINER_USERNAME,
                                 email='maintainer@gmail.com')
            user.set_password(PASSWORD)
       
            maintainer_gp.user_set.add(user)
            user.save()

        if not User.objects.filter(username__iexact=REQUESTOR_USERNAME).exists():
            user = User.objects.create(username=REQUESTOR_USERNAME,
                                 email='requestor@gmail.com')
            user.set_password(PASSWORD)

            requester_gp.user_set.add(user)
            user.save()

        