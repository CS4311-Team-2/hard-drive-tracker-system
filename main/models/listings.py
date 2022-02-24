from django.db import models
from django.utils.timezone import now
from datetime import datetime

#TODO Remove, Template code. 
class Listings(models.Model):

    class SaleType(models.TextChoices):
        PICK_UP = "Available for pickup"
        SHIP = "Available for shipping"

    class ConditionType(models.TextChoices):
        USED = "Used"
        NEW = "New"

    class ProductType(models.TextChoices):
        BIKE = "Bike"
        PARTS = "Parts"
        MODELS = "Models"
        OTHER = "Other"

  
    title = models.CharField(max_length=100)
    condition = models.CharField(
        max_length=50, choices=ConditionType.choices, default=ConditionType.USED)
    product_type = models.CharField(
        max_length=50, choices=ProductType.choices, default=ProductType.BIKE)
    sale_type = models.CharField(
        max_length=50, choices=SaleType.choices, default=SaleType.SHIP)
    price = models.FloatField()
    address = models.CharField(max_length=100)
    city = models.CharField(max_length=25)
    state = models.CharField(max_length=25)
    zipcode = models.CharField(max_length=25)
    list_date = models.DateTimeField(default=now)
    contact_email = models.CharField(max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = "Listings"