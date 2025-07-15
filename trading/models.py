from django.db import models
from django.contrib.auth.models import User

class Cryptocurrency(models.Model):
    name = models.CharField(max_length=50)  # Bitcoin, Ethereum, etc.
    symbol = models.CharField(max_length=10)  # BTC, ETH, etc.
    total_supply = models.DecimalField(max_digits=20, decimal_places=8)
    current_price = models.DecimalField(max_digits=20, decimal_places=8)
    wallet_address = models.CharField(max_length=100, blank=True, null=True)
    price_change_24h = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.name} ({self.symbol})"
    
    class Meta:
        verbose_name_plural = "Cryptocurrencies"

class Portfolio(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=20, decimal_places=8, default=0)
    total_invested = models.DecimalField(max_digits=20, decimal_places=2, default=0)
    
    class Meta:
        unique_together = ['user', 'cryptocurrency']
    
    @property
    def current_value(self):
        return self.balance * self.cryptocurrency.current_price
    
    @property
    def profit_loss(self):
        return self.current_value - self.total_invested
    
    @property
    def profit_loss_percentage(self):
        if self.total_invested > 0:
            return (self.profit_loss / self.total_invested) * 100
        return 0

class PriceHistory(models.Model):
    cryptocurrency = models.ForeignKey(Cryptocurrency, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=20, decimal_places=8)
    timestamp = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-timestamp']