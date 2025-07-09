from django import forms
from .models import Cryptocurrency

class CryptocurrencyForm(forms.ModelForm):
    class Meta:
        model = Cryptocurrency
        fields = ['name', 'symbol', 'total_supply', 'current_price']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'symbol': forms.TextInput(attrs={'class': 'form-control', 'style': 'text-transform: uppercase;'}),
            'total_supply': forms.NumberInput(attrs={'class': 'form-control'}),
            'current_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00000001'}),
        }

class PriceUpdateForm(forms.Form):
    UPDATE_TYPE_CHOICES = [
        ('percentage', 'Percentage Change'),
        ('direct', 'Direct Price'),
    ]
    
    update_type = forms.ChoiceField(choices=UPDATE_TYPE_CHOICES, widget=forms.RadioSelect)
    percentage = forms.DecimalField(max_digits=5, decimal_places=2, required=False, 
                                   widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01'}))
    new_price = forms.DecimalField(max_digits=20, decimal_places=8, required=False,
                                  widget=forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00000001'}))
