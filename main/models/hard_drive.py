from email.policy import default
from django.db import models
from unixtimestampfield.fields import UnixTimeStampField
from .request import Request

# Hard Drive model
class HardDrive(models.Model):
    
    class Classification(models.TextChoices):
        CLASSIFIED = "classified"
        UNCLASSIFIED = "unclassified"

    class BootTestStatus(models.TextChoices):
        PASS = "pass"
        FAILED = "failed"

    class ConnectionPort(models.TextChoices):
        SATA = "SATA"
        M2 = "M.2"

    create_date = UnixTimeStampField(auto_now_add=True) 
    serial_number = models.CharField(max_length=100)
    manufacturer = models.CharField(blank=True, max_length=100)
    model_number = models.CharField(blank=True, max_length=100)
    hard_drive_type = models.CharField(max_length=100)
    connection_port = models.CharField(max_length=100)
    hard_drive_size = models.CharField(max_length=100)
    classification = models.CharField(max_length=50, choices=Classification.choices, 
                                        default=Classification.UNCLASSIFIED)
    # TODO(django): This field needs to be changed when the classification is changed. 
    justification_for_classification_change = models.TextField(blank=True)
    # TODO(django): Need to limit this number at 4. 
    hard_drive_image = models.CharField(blank=True, max_length=100)
    image_version_id = models.CharField(max_length=100)
    boot_test_status = models.CharField(max_length=50, choices=BootTestStatus.choices, 
                                            default=BootTestStatus.PASS)
    boot_test_expiration = UnixTimeStampField(use_numeric=True, default=0.0)

    # The options to this field can be configured. 
    status = models.CharField(max_length=100)
    justification_for_hard_drive_status_change = models.TextField(blank=True)
    issue_date = UnixTimeStampField(default=0.0)
    expected_hard_drive_return_date = UnixTimeStampField(default=0.0)
    justification_for_hard_drive_return_date = models.TextField(blank=True)
    actual_return_date = UnixTimeStampField(default=0.0)
    modified_date = UnixTimeStampField(auto_now=True, auto_now_add=True)
    request = models.ForeignKey(Request, 
                    on_delete=models.CASCADE, null=True, blank=True, related_name="hard_drives")

    class Meta:
        verbose_name_plural = "Hard Drive"


     #TODO Need to add foreign key to request.