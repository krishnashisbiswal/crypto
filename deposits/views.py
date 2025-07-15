from django.http.response import JsonResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView
from django.contrib import messages
from django.utils import timezone
from .models import Deposit, Cryptocurrency
from .forms import DepositForm
from trading.models import Portfolio
from referrals.models import ReferralCommission
from django.db.models import Sum

@login_required
def deposit_create(request):
    wallet_address = None  # always define

    if request.method == "POST":
        form = DepositForm(request.POST)
        if form.is_valid():
            deposit = form.save(commit=False)
            deposit.user = request.user

            coin = deposit.cryptocurrency  # user selected coin
            wallet_address = coin.wallet_address  # get from DB
            deposit.wallet_address = wallet_address
            deposit.save()

            messages.success(request, "Deposit submitted!")
            return redirect('deposits:deposit_list')
    else:
        form = DepositForm()

    # 🗝️ If user selected coin in GET, show it too (optional):
    if 'cryptocurrency' in request.GET:
        coin_id = request.GET['cryptocurrency']
        try:
            coin = Cryptocurrency.objects.get(pk=coin_id)
            wallet_address = coin.wallet_address
        except Cryptocurrency.DoesNotExist:
            wallet_address = None

    return render(request, "deposits/create.html", {
        "form": form,
        "wallet_address": wallet_address,
    })

def deposit_list(request):
    if request.user.is_superuser:
        # Admin sees all deposits
        deposits = Deposit.objects.all()
        template_name = 'deposits/admin/list.html'
    else:
        # Regular user sees only their deposits
        deposits = Deposit.objects.filter(user=request.user)
        
        template_name = 'deposits/list.html'

    context = {
        'deposits': deposits,
        'total_deposits': deposits.count(),
        'pending_count': deposits.filter(status='pending').count(),
        'approved_count': deposits.filter(status='approved').count(),
        'rejected_count': deposits.filter(status='rejected').count(),
        'total_approved_value': deposits.filter(status='approved').aggregate(total=Sum('amount'))['total'] or 0,
    }
    return render(request, template_name, context)



@user_passes_test(lambda u: u.is_superuser)
def admin_deposit_list(request):
    # This is for superusers to see all deposits
    deposits = Deposit.objects.all()
    return render(request, 'deposits/admin/list.html', {'deposits': deposits})

# Admin Views
class AdminDepositListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Deposit
    template_name = 'deposits/admin/list.html'
    context_object_name = 'deposits'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def get_queryset(self):
        return Deposit.objects.all().select_related('user', 'cryptocurrency').order_by('-created_at')

@user_passes_test(lambda u: u.is_superuser)
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

def admin_approve_deposit(request, deposit_id):
    deposit = get_object_or_404(Deposit, id=deposit_id)
    deposit.status = 'approved'
    deposit.save()
    messages.success(request, f'Deposit of ${deposit.amount} approved for {deposit.user.username}')
    return redirect('deposits:admin_list')

def admin_reject_deposit(request, deposit_id):
    deposit = get_object_or_404(Deposit, id=deposit_id)
    deposit.status = 'rejected'
    deposit.save()
    messages.error(request, f'Deposit of ${deposit.amount} rejected for {deposit.user.username}')
    return redirect('deposits:admin_list')

def get_wallet_address(request, coin_id):
    try:
        coin = Cryptocurrency.objects.get(pk=coin_id)
        return JsonResponse({'wallet_address': coin.wallet_address})
    except Cryptocurrency.DoesNotExist:
        return JsonResponse({'wallet_address': ''})
    
# @user_passes_test(lambda u: u.is_staff)
# def admin_update_deposit_status(request, deposit_id):
#     deposit = get_object_or_404(Deposit, id=deposit_id)

#     if request.method == 'POST':
#         status = request.POST.get('status')
#         if status in ['approved', 'rejected']:
#             deposit.status = status
#             deposit.save()
#             messages.success(request, f"Deposit {status.capitalize()} successfully.")
#         else:
#             messages.error(request, "Invalid status value.")

#     return redirect('deposits:admin_deposit_list')