from lib2to3.pytree import Base
from django.core.management.base import BaseCommand
import pandas as pd
from main.models.hard_drive import HardDrive

class Command(BaseCommand):
    help = 'import booms'

    def add_arguments(self, parser):
        pass

    def handle(self, *args, **options):
        df = pd.read_csv('hard_drives.csv')
        for id, create_date, serial_number, manufacturer, model_number, hard_drive_type, connection_port, hard_drive_size, classification, justification_for_classification_change, imange_version_id, boot_test_status, boot_test_expiration, status, justification_for_hard_drive_status_change, issue_date, expected_hard_drive_return_date, justification_for_hard_drive_return_date_status_change, actual_return_date, modified_date in zip(df.id, df.create_date, df.serial_number, df.manufacturer, df.model_number, df.hard_drive_type, df.connection_port, df.hard_drive_size, df.classification, df.justification_for_classification_change, df.imange_version_id, df.boot_test_status, df.boot_test_expiration, df.status, df.justification_for_hard_drive_status_change, df.issue_date, df.expected_hard_drive_return_date, df.justification_for_hard_drive_return_date_status_change, df.actual_return_date, df.modified_date):
            models = HardDrive(id, create_date, serial_number, manufacturer, model_number, hard_drive_type, connection_port, hard_drive_size, classification, justification_for_classification_change, imange_version_id, boot_test_status, boot_test_expiration, status, justification_for_hard_drive_status_change, issue_date, expected_hard_drive_return_date, justification_for_hard_drive_return_date_status_change, actual_return_date, modified_date)
            models.save()