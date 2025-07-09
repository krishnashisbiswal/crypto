from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.db.models import Sum, Count
from .models import ReferralCommission
from accounts.models import UserProfile

@login_required
def referral_dashboard(request):
    try:
        user_profile = request.user.userprofile
    except UserProfile.DoesNotExist:
        # Create profile if it doesn't exist
        user_profile = UserProfile.objects.create(user=request.user)
    
    # Get referral statistics with error handling
    total_commissions = ReferralCommission.objects.filter(user=request.user).aggregate(
        total=Sum('amount')
    )['total'] or 0
    
    # Get referrals by level
    level_commissions = {}
    for level in [1, 2, 3]:
        level_total = ReferralCommission.objects.filter(
            user=request.user, level=level
        ).aggregate(total=Sum('amount'))['total'] or 0
        level_commissions[level] = level_total
    
    # Get recent commissions
    recent_commissions = ReferralCommission.objects.filter(
        user=request.user
    ).select_related('referred_user', 'deposit').order_by('-created_at')[:10]
    
    # Get direct referrals (people who used your referral code)
    direct_referrals = UserProfile.objects.filter(referred_by=user_profile)
    
    # Get referral statistics
    total_referrals = direct_referrals.count()
    
    # Debug information
    debug_info = {
        'user_has_profile': bool(user_profile),
        'referral_code': user_profile.referral_code if user_profile else 'None',
        'total_commissions_count': ReferralCommission.objects.filter(user=request.user).count(),
        'direct_referrals_count': total_referrals,
        'recent_commissions_count': recent_commissions.count(),
    }
    
    context = {
        'user_profile': user_profile,
        'total_commissions': total_commissions,
        'level_commissions': level_commissions,
        'recent_commissions': recent_commissions,
        'direct_referrals': direct_referrals,
        'total_referrals': total_referrals,
        'debug_info': debug_info,
        'referral_url': f"http://localhost:8000/accounts/register/?ref={user_profile.referral_code}" if user_profile else "",
    }
    
    return render(request, 'referrals/dashboard.html', context)

