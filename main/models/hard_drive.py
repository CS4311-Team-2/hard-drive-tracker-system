from email.policy import default
from django.db import models
from django.utils import timezone
from unixtimestampfield.fields import UnixTimeStampField


#TODO: Need to create options for status, connection port, classification, 
# and boot_test_status 
class HardDrive(models.Model):
    
    class Classification(models.TextChoices):
        CLASSIFIED = "classified"
        UNCLASSIFIED = "unclassified"

    class BootTestStatus(models.TextChoices):
        PASS = "pass"
        FAILED = "failed"

    hard_drive_id = models.TextField(primary_key=True)
    # TODO: Make sure this field when the object is created. 
    create_date = UnixTimeStampField(auto_now_add=True) 
    serial_number = models.CharField(max_length=100)
    manufacturer = models.CharField(blank=True, max_length=100)
    model_number = models.CharField(blank=True, max_length=100)
    hard_drive_type = models.CharField(max_length=100)
    connection_port = models.CharField(max_length=100)
    hard_drive_size = models.CharField(max_length=100)
    classification = models.CharField(max_length=50, choices=Classification.choices, 
                                        default=Classification.UNCLASSIFIED)
    # This field needs to be changed when the classification is changed. 
    # TODO: This needs to give the option of a file or straight text. 
    justification_for_classification_change = models.TextField()
    # TODO: Need to limit this number at 4. 
    image_version_id = models.CharField(max_length=100)
    boot_test_status = models.CharField(max_length=50, choices=BootTestStatus.choices, 
                                            default=BootTestStatus.PASS)
    boot_test_expiration = UnixTimeStampField(blank=True)

    # The options to this field can be configured. 
    status = models.CharField(max_length=100)
    justification_for_hard_drive_status_change = models.TextField(blank=True)
    issue_date = UnixTimeStampField(blank=True)
    expected_hard_drive_return_date = UnixTimeStampField(blank=True)
    justification_for_hard_drive_return_date_status_change = models.TextField(blank=True)
    actual_return_date = UnixTimeStampField(blank=True)
    modified_date = UnixTimeStampField(auto_now=True, auto_now_add=True)

    class Meta:
        verbose_name_plural = "Hard Drive"


     #TODO Need to add foreign key to request.