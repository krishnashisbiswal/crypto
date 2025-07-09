from django import forms
from .models import Deposit
from trading.models import Cryptocurrency

class DepositForm(forms.ModelForm):
    class Meta:
        model = Deposit
        fields = ['cryptocurrency', 'amount', 'transaction_hash', 'wallet_address']
        widgets = {
            'cryptocurrency': forms.Select(attrs={'class': 'form-control'}),
            'amount': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}),
            'transaction_hash': forms.TextInput(attrs={'class': 'form-control'}),
            'wallet_address': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cryptocurrency'].queryset = Cryptocurrency.objects.filter(is_active=True)
