from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """
    Custom user model extending Django's built-in AbstractUser.
    Adds user_type (buyer/seller), company_name, phone, address, profile_picture.
    """

    USER_TYPE_CHOICES = (
        ('buyer', 'Buyer'),
        ('seller', 'Seller'),
    )

    user_type = models.CharField(
        max_length=10,
        choices=USER_TYPE_CHOICES,
        default='buyer'
    )
    company_name = models.CharField(
        max_length=255,
        blank=True,
        null=True,
        help_text='Required for sellers only'
    )
    phone = models.CharField(max_length=20, blank=True, null=True)
    address = models.CharField(max_length=500, blank=True, null=True)
    profile_picture = models.ImageField(
        upload_to='profile_pictures/',
        blank=True,
        null=True
    )

    def is_seller(self):
        return self.user_type == 'seller'

    def is_buyer(self):
        return self.user_type == 'buyer'

    def __str__(self):
        return f"{self.username} ({self.user_type})"
# Create your models here.
