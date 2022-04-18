from email.policy import default
from django.db import models
from django.utils import timezone
from django.conf import settings
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

    class Status(models.TextChoices):
        ASSIGNED = 'Assigned'
        AVAILABLE = 'Available'
        END_OF_LIFE = 'End of Life'
        MASTER = 'Master Clone'
        PENDING_WIPE = 'Pending Wipe'
        DESTROYED = "Destroyed"
        LOST = 'Lost'
        OVERDUE = 'Overdue'
        PICKED_UP = 'Picked Up'
        RETUREND = 'Returned'
        PENDING_CLASSIFICATION_CHANGE_APPROVAL = 'Pending Classification Change Approval'

    create_date = models.DateField(default=timezone.now, blank=True) 
    serial_number = models.CharField(unique=True, max_length=100)
    manufacturer = models.CharField(blank=True, max_length=100)
    model_number = models.CharField(blank=True, max_length=100)
    hard_drive_type = models.CharField(max_length=100)  
    connection_port = models.CharField(max_length=100)
    hard_drive_size = models.CharField(max_length=100)
    classification = models.CharField(max_length=50, choices=Classification.choices, 
                                        default=Classification.UNCLASSIFIED)
    # TODO(django): This field needs to be changed when the classification is changed. 
    justification_for_classification_change = models.TextField(default='')
    # TODO(django): Need to limit this number at 4.     
    hard_drive_image = models.CharField(blank=True, max_length=100)
    image_version_id = models.CharField(max_length=100)
    boot_test_status = models.CharField(max_length=50, choices=BootTestStatus.choices, 
                                            default=BootTestStatus.PASS)
    boot_test_expiration = models.DateField(default=timezone.now, blank=True )

    # The options to this field can be configured. 
    status = models.CharField(max_length=100, choices=Status.choices, default=Status.AVAILABLE)
    justification_for_hard_drive_status_change = models.TextField(blank=True)
    issue_date = models.DateField(blank=True)
    expected_hard_drive_return_date = models.DateField(default=timezone.now, blank=True)
    justification_for_hard_drive_return_date = models.TextField(blank=True)
    actual_return_date = models.DateField(blank=True)
    modified_date = models.DateField(default=timezone.now, blank=True)
    modifier = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE) 
    request = models.ForeignKey(Request, 
                    on_delete=models.CASCADE, null=True, blank=True, related_name="hard_drives")    
    # Manually save. 
    def save(self, *args, **kwargs):
        if self.create_date is None:
            self.create_date = timezone.now()
            print("Succesfully saved create date")
        self.modified_date = timezone.now()
        
        super(HardDrive, self).save(*args, **kwargs)
    class Meta:
        verbose_name_plural = "Hard Drive"
    