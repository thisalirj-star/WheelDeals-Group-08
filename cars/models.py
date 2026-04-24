from django.db import models
from django.conf import settings


class Car(models.Model):
    """
    Car listing model.
    Uses settings.AUTH_USER_MODEL instead of importing User directly
    so other apps don't get circular import issues.
    """

    VEHICLE_TYPE_CHOICES = (
        ('sedan', 'Sedan'),
        ('suv', 'SUV'),
        ('hatchback', 'Hatchback'),
        ('coupe', 'Coupe'),
        ('truck', 'Truck'),
        ('van', 'Van'),
        ('convertible', 'Convertible'),
        ('wagon', 'Wagon'),
    )

    FUEL_TYPE_CHOICES = (
        ('petrol', 'Petrol'),
        ('diesel', 'Diesel'),
        ('electric', 'Electric'),
        ('hybrid', 'Hybrid'),
        ('lpg', 'LPG'),
    )

    CONDITION_CHOICES = (
        ('new', 'New'),
        ('used', 'Used'),
        ('certified', 'Certified Pre-Owned'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField()
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    mileage = models.IntegerField(help_text='Mileage in km')
    vehicle_type = models.CharField(max_length=50, choices=VEHICLE_TYPE_CHOICES)
    fuel_type = models.CharField(max_length=50, choices=FUEL_TYPE_CHOICES)
    condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    starting_price = models.DecimalField(max_digits=12, decimal_places=2)
    sold_price = models.DecimalField(
        max_digits=12, decimal_places=2,
        null=True, blank=True
    )
    location = models.CharField(max_length=255)
    image = models.ImageField(upload_to='car_images/', blank=True, null=True)

    # seller and sold_to use settings.AUTH_USER_MODEL — safer for team projects
    seller = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='cars_listed'
    )
    sold_to = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True, blank=True,
        related_name='cars_bought'
    )

    auction_end_time = models.DateTimeField(null=True, blank=True)
    is_sold = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.year} {self.brand} {self.model} — {self.title}"

    class Meta:
        ordering = ['-created_at']

class CarImage(models.Model):
    """
    Stores multiple images for a single car listing.
    A car can have up to 5 images.
    """
    car = models.ForeignKey(
        Car,
        on_delete=models.CASCADE,
        related_name='images'
    )
    image = models.ImageField(upload_to='car_images/')
    is_primary = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.car.title}"

