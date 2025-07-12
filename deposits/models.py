from django.db import models
from django.contrib.auth.models import User
from trading.models import Cryptocurrency

class Deposit(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    transaction_hash = models.CharField(max_length=100, blank=True)
    wallet_address = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    price_at_deposit = models.DecimalField(max_digits=20, decimal_places=10, default=0)
    coin_quantity = models.DecimalField(max_digits=20, decimal_places=10, default=0)

    def save(self, *args, **kwargs):
        if not self.price_at_deposit:
            self.price_at_deposit = self.cryptocurrency.current_price
        if not self.coin_quantity:
            self.coin_quantity = self.amount / self.price_at_deposit
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.user.username} - ${self.amount} - {self.status}"