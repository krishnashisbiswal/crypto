from django.db import models
from django.contrib.auth.models import User
from deposits.models import Deposit

class ReferralCommission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Who receives commission
    referred_user = models.ForeignKey(User, related_name='referrals_given', on_delete=models.CASCADE)  # Who was referred
    level = models.IntegerField()  # 1, 2, or 3
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    deposit = models.ForeignKey(Deposit, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} - Level {self.level} - ${self.amount}"
