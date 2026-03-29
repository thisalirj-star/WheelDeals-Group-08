from django.db import models
from django.contrib.auth.models import User

class Car(models.Model):

    VEHICLE_TYPE_CHOICES = [
        ('Car', 'Car'),
        ('Van', 'Van'),
        ('Motorcycle/Scooter', 'Motorcycle/Scooter'),
        ('Three Wheeler', 'Three Wheeler'),
        ('Lorry', 'Lorry'),
    ]

    CONDITION_CHOICES = [
        ('Brand New', 'Brand New'),
        ('Registered', 'Registered'),
        ('Unregistered', 'Unregistered'),
    ]

    FUEL_TYPE_CHOICES = [
        ('Petrol', 'Petrol'),
        ('Diesel', 'Diesel'),
        ('Electric', 'Electric'),
        ('Hybrid', 'Hybrid'),
        ('Other', 'Other'),
    ]

    # Basic info
    title = models.CharField(max_length=200)
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_TYPE_CHOICES)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    fuel_type = models.CharField(max_length=50, choices=FUEL_TYPE_CHOICES)
    mileage = models.IntegerField(help_text="Mileage in km")

    # Pricing
    starting_price = models.DecimalField(max_digits=12, decimal_places=2)

    # Description & location
    description = models.TextField()
    location = models.CharField(max_length=200)

    # Images
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)

    # Seller info
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cars')
    seller_contact = models.CharField(max_length=100)

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    is_sold = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.title} - {self.brand} {self.model} ({self.year})"