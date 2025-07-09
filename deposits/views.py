from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView
from django.contrib import messages
from django.utils import timezone
from .models import Deposit
from .forms import DepositForm
from trading.models import Portfolio
from referrals.models import ReferralCommission

@login_required
def deposit_create(request):
    if request.method == 'POST':
        form = DepositForm(request.POST)
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user = request.user
            deposit.save()
            messages.success(request, 'Deposit request submitted successfully!')
            return redirect('deposits:deposit_list')
    else:
        form = DepositForm()
    return render(request, 'deposits/create.html', {'form': form})

@login_required
def deposit_list(request):
    deposits = Deposit.objects.filter(user=request.user).order_by('-created_at')
    pending_count = deposits.filter(status='pending').count()
    approved_count = deposits.filter(status='approved').count()
    rejected_count = deposits.filter(status='rejected').count()
    total_count = deposits.count()

    return render(request, 'deposits/list.html', {
        'deposits': deposits,
        'pending_count': pending_count,
        'approved_count': approved_count,
        'rejected_count': rejected_count,
        'total_count': total_count
    })

# Admin Views
class AdminDepositListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Deposit
    template_name = 'deposits/admin/list.html'
    context_object_name = 'deposits'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_queryset(self):
        return Deposit.objects.all().select_related('user', 'cryptocurrency').order_by('-created_at')

@user_passes_test(lambda u: u.is_staff)
def approve_deposit(request, deposit_id):
    deposit = get_object_or_404(Deposit, pk=deposit_id)
    
    if deposit.status == 'pending':
        # Calculate coins to add
        coins_to_add = deposit.amount / deposit.cryptocurrency.current_price
        
        # Update or create portfolio
        portfolio, created = Portfolio.objects.get_or_create(
            user=deposit.user,
            cryptocurrency=deposit.cryptocurrency,
            defaults={'balance': 0, 'total_invested': 0}
        )
        
        portfolio.balance += coins_to_add
        portfolio.total_invested += deposit.amount
        portfolio.save()
        
        # Process referral commissions
        process_referral_commissions(deposit)
        
        # Update deposit
        deposit.status = 'approved'
        deposit.approved_at = timezone.now()
        deposit.save()
        
        messages.success(request, f'Deposit of ${deposit.amount} approved for {deposit.user.username}')
    
    return redirect('deposits:admin_list')

def process_referral_commissions(deposit):
    user_profile = deposit.user.userprofile
    current_referrer = user_profile.referred_by
    level = 1
    commission_rates = [5, 3, 2]  # 5%, 3%, 2%
    
    while current_referrer and level <= 3:
        commission_percentage = commission_rates[level - 1]
        commission_amount = deposit.amount * (commission_percentage / 100)
        
        ReferralCommission.objects.create(
            user=current_referrer.user,
            referred_user=deposit.user,
            level=level,
            amount=commission_amount,
            deposit=deposit
        )
        
        current_referrer = current_referrer.referred_by
        level += 1

@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_deposit_status(request, deposit_id):
    deposit = get_object_or_404(Deposit, id=deposit_id)

    # Only allow if user is admin/staff or deposit owner
    if not (request.user.is_staff or deposit.user == request.user.is_superuser):
        messages.error(request, "You don't have permission to perform this action.")
        return redirect('deposits:deposit_list')

    if request.method == 'POST':
        status = request.POST.get('status')
        if status in ['approved', 'rejected']:
            deposit.status = status
            deposit.save()
            messages.success(request, f"Deposit {status.capitalize()} successfully.")
        else:
            messages.error(request, "Invalid status value.")
    return redirect('deposits:deposit_list')

def is_admin(user):
    return user.is_staff or user.is_superuser

@login_required
def user_deposits_list(request):
    deposits = Deposit.objects.filter(user=request.user)
    return render(request, 'deposits/list.html', {'deposits': deposits})

@login_required
@user_passes_test(is_admin)
def admin_deposits_list(request):
    deposits = Deposit.objects.all()
    return render(request, 'deposits/admin/list.html', {'deposits': deposits})