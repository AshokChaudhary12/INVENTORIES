from django.core.validators import FileExtensionValidator
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.


class User(AbstractUser):
    COOICES_FILDS = (
        ('O', 'Office'),
        ('S', 'School'),
        ('H', 'Hospital'),
    )
    inventories = models.CharField(max_length=100, choices=COOICES_FILDS, default='O')
    email = models.EmailField(max_length=30, unique=True)


class InventoriesTypes(models.Model):
    COOICES_FILDS = (
        ('O', 'Office'),
        ('S', 'School'),
        ('H', 'Hospital'),
    )
    type = models.CharField(max_length=100, choices=COOICES_FILDS, default='O')
    name = models.CharField(max_length=20, null=False)

    def __str__(self):
        return f" {self.name}"


class InventoryImage(models.Model):
    image = models.FileField(upload_to='Inventories/images', null=True, blank=True,
                             validators=[FileExtensionValidator(['png', 'jpg', 'svg'])])


class Inventories(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user_inventories")
    inventry_type = models.ForeignKey(InventoriesTypes, on_delete=models.CASCADE)
    name = models.CharField(max_length=20, null=True)
    quantity = models.PositiveIntegerField(null=True)
    purchase_date = models.DateField()
    created_date = models.DateField(auto_now=True)
    unit_price = models.DecimalField(max_digits=20, decimal_places=2)
    images = models.ManyToManyField(InventoryImage, related_name='Inventories_images')
    is_delete = models.BooleanField(default=False)

    def __str__(self):
        return self.name
