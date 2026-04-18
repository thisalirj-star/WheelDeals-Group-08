from django.db import models
from django.contrib.auth.models import User

# FUTURE (when Car model is ready)
# from cars.models import Car
# car = models.ForeignKey(Car, on_delete=models.CASCADE)

class Bid(models.Model):
    car = models.ForeignKey('cars.Car', on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    # TEMP FIX (NO FOREIGN KEY)
    #car_id = models.IntegerField()

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.amount}"