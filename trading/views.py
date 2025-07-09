from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Sum
from .models import Cryptocurrency, Portfolio, PriceHistory
from .forms import CryptocurrencyForm, PriceUpdateForm
import json
from decimal import Decimal
def is_staff(user):
    return user.is_staff

@login_required
def dashboard(request):
    portfolios = Portfolio.objects.filter(user=request.user).select_related('cryptocurrency')
    total_value = sum([p.current_value for p in portfolios])
    total_invested = sum([p.total_invested for p in portfolios])
    total_profit_loss = total_value - total_invested
    
    context = {
        'portfolios': portfolios,
        'total_value': total_value,
        'total_invested': total_invested,
        'total_profit_loss': total_profit_loss,
        'total_profit_loss_percentage': (total_profit_loss / total_invested * 100) if total_invested > 0 else 0,
    }
    return render(request, 'trading/dashboard.html', context)

@login_required
def price_chart(request, crypto_id):
    crypto = get_object_or_404(Cryptocurrency, pk=crypto_id)
    price_history = PriceHistory.objects.filter(cryptocurrency=crypto).order_by('-timestamp')[:30]
    
    chart_data = {
        'labels': [p.timestamp.strftime('%Y-%m-%d %H:%M') for p in reversed(price_history)],
        'prices': [float(p.price) for p in reversed(price_history)],
        'crypto_name': crypto.name,
        'crypto_symbol': crypto.symbol,
        'current_price': float(crypto.current_price),
        'price_change': float(crypto.price_change_24h),
    }
    
    return JsonResponse(chart_data)

# Admin Views
class CryptocurrencyListView(LoginRequiredMixin, UserPassesTestMixin, ListView):
    model = Cryptocurrency
    template_name = 'trading/admin/crypto_list.html'
    context_object_name = 'cryptocurrencies'
    
    def test_func(self):
        return self.request.user.is_staff

class CryptocurrencyCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Cryptocurrency
    form_class = CryptocurrencyForm
    template_name = 'trading/admin/crypto_form.html'
    success_url = '/trading/admin/cryptocurrencies/'
    
    def test_func(self):
        return self.request.user.is_staff
    
    def form_valid(self, form):
        messages.success(self.request, f"{form.instance.name} added successfully!")
        return super().form_valid(form)

@user_passes_test(is_staff)
def price_update(request, crypto_id):
    crypto = get_object_or_404(Cryptocurrency, pk=crypto_id)
    
    if request.method == 'POST':
        form = PriceUpdateForm(request.POST)
        if form.is_valid():
            update_type = form.cleaned_data['update_type']
            
            if update_type == 'percentage':
                percentage = Decimal(str(form.cleaned_data['percentage']))
                new_price = crypto.current_price * (Decimal('1') + percentage / Decimal('100'))
                crypto.price_change_24h = float(percentage)
            else:  # direct
                new_price = Decimal(str(form.cleaned_data['new_price']))
                old_price = crypto.current_price
                percentage = ((new_price - old_price) / old_price) * Decimal('100')
                crypto.price_change_24h = float(percentage)
            
            crypto.current_price = new_price
            crypto.save()
            
            # Save to history
            PriceHistory.objects.create(cryptocurrency=crypto, price=new_price)
            
            messages.success(request, f"{crypto.symbol} price updated to ${new_price}")
            return redirect('trading:admin_crypto_list')
    else:
        form = PriceUpdateForm()
    price_history = PriceHistory.objects.filter(cryptocurrency=crypto).order_by('-timestamp')[:10]

    return render(request, 'trading/admin/price_update.html', {
        'form': form, 
        'crypto': crypto,
        'price_history': price_history
    })