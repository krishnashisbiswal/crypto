from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm, KYCForm
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy

class RoleBasedLoginView(LoginView):
    template_name = 'registration/login.html'  # adjust if your template is different

    def get_success_url(self):
        """Decide where to send the user after login based on their role."""
        user = self.request.user
        if user.is_superuser:
            return reverse_lazy('trading:admin_dashboard')
        else:
            return reverse_lazy('trading:dashboard')

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            if user.is_superuser:
                return redirect('trading:admin_dashboard')
            else:
                return redirect('trading:dashboard')
    else:
        form = CustomUserCreationForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')

@login_required
def kyc_upload(request):
    if request.method == 'POST':
        form = KYCForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            messages.success(request, 'KYC document uploaded successfully!')
            return redirect('accounts:profile')
    else:
        form = KYCForm(instance=request.user.userprofile)
    return render(request, 'accounts/kyc_upload.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('accounts:login')

def home(request):
    return render(request, 'home/index.html')

def about(request):
    return render(request, 'home/about.html')

def faq(request):
    return render(request, 'home/faq.html')

def terms(request):
    return render(request, 'home/terms.html')

def vision(request):
    return render(request, 'home/vision.html')

def revolution(request):
    return render(request, 'home/revolution.html')