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
    amount = models.DecimalField(max_digits=20, decimal_places=2)  # Amount in USD
    transaction_hash = models.CharField(max_length=100, blank=True)
    wallet_address = models.CharField(max_length=50)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    approved_at = models.DateTimeField(null=True, blank=True)
    
    @property
    def coins_to_receive(self):
        return self.amount / self.cryptocurrency.current_price
    
    def __str__(self):
        return f"{self.user.username} - ${self.amount} - {self.status}"
