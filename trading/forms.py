# trading/forms.py
from django import forms
from .models import Cryptocurrency
from decimal import Decimal

class CryptocurrencyForm(forms.ModelForm):
    class Meta:
        model = Cryptocurrency
        fields = ['name', 'symbol', 'total_supply', 'current_price', 'is_active', 'wallet_address']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., Bitcoin'}),
            'symbol': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g., BTC'}),
            'total_supply': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00000001'}),
            'current_price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.00000001'}),
            'is_active': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'wallet_address': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Receiving Wallet Address'}),
        }

class PriceUpdateForm(forms.Form):
    update_type = forms.ChoiceField(
        choices=[('percentage', 'Percentage Change'), ('direct', 'Direct Entry')],
        widget=forms.RadioSelect(attrs={'class': 'form-check-input'}),
        required=True
    )

    percentage = forms.DecimalField(
        max_digits=5,
        decimal_places=2,
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., 5.5',
            'step': '0.01'
        }),
        label='Percentage Change (%)'
    )

    new_price = forms.DecimalField(
        max_digits=20,
        decimal_places=8,
        min_value=Decimal('0.00000001'),
        required=False,
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter new price',
            'step': '0.00000001'
        }),
        label='New Price (₹)'
    )

    def clean(self):
        cleaned_data = super().clean()
        update_type = cleaned_data.get('update_type')

        if update_type == 'percentage' and cleaned_data.get('percentage') is None:
            self.add_error('percentage', 'Please provide a percentage value.')

        if update_type == 'direct' and cleaned_data.get('new_price') is None:
            self.add_error('new_price', 'Please provide the new price.')

        return cleaned_data