from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=30, required=True)
    last_name = forms.CharField(max_length=30, required=True)
    phone = forms.CharField(max_length=20, required=False)
    referral_code = forms.CharField(max_length=10, required=False)
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'phone', 'email', 'password1', 'password2', 'referral_code')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
            profile = user.userprofile
            profile.phone = self.cleaned_data['phone']
            
            # Handle referral
            referral_code = self.cleaned_data.get('referral_code')
            if referral_code:
                try:
                    referrer = UserProfile.objects.get(referral_code=referral_code)
                    profile.referred_by = referrer
                except UserProfile.DoesNotExist:
                    pass
            
            profile.save()
        return user

class KYCForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['kyc_document']
