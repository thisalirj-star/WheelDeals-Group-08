from django.db import models
from django.conf import settings
from django.utils import timezone
from datetime import timedelta


class Auction(models.Model):

    DURATION_CHOICES = [
        ('6',  '6 Hours'),
        ('12', '12 Hours'),
        ('24', '24 Hours'),
        ('72', '3 Days'),
    ]

    STATUS_CHOICES = [
        ('ACTIVE', 'Active'),
        ('PAUSED', 'Paused'),
        ('ENDED',  'Ended'),
    ]

    # Temporary: plain IntegerField until cars app is merged
    car_id = models.IntegerField(null=True, blank=True)

    duration = models.CharField(max_length=5, choices=DURATION_CHOICES, default='6')

    end_time   = models.DateTimeField(null=True, blank=True)
    status     = models.CharField(max_length=10, choices=STATUS_CHOICES, default='ACTIVE')
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.pk and not self.end_time:
            self.end_time = timezone.now() + timedelta(hours=int(self.duration))
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Auction #{self.pk} ({self.status})"


class Bid(models.Model):

    auction = models.ForeignKey(
        Auction,
        on_delete=models.CASCADE,
        related_name='bids',
        null=True, blank=True
    )

    buyer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='bids',
        null=True, blank=True
    )

    amount     = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-amount']

    def __str__(self):
        return f"{self.buyer.username}: ${self.amount} on Auction #{self.auction.pk}"