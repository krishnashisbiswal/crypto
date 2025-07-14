from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import ListView, CreateView, UpdateView
from django.http import JsonResponse
from django.contrib import messages
from decimal import Decimal
from .models import Cryptocurrency, PriceHistory
from .forms import CryptocurrencyForm, PriceUpdateForm
from deposits.models import Deposit  # ✅ Corrected this line
from django.utils.timezone import now  # ✅ Added for last_updated
from django.views.decorators.http import require_POST
from django.views.generic import DetailView

def is_staff(user):
    return user.is_staff

@login_required
def dashboard(request):
    user = request.user
    deposits = Deposit.objects.filter(user=user, status='approved')

    portfolio_dict = {}

    for dep in deposits:
        crypto = dep.cryptocurrency
        symbol = crypto.symbol

        if symbol not in portfolio_dict:
            portfolio_dict[symbol] = {
                'cryptocurrency': crypto,
                'balance': Decimal('0'),
                'total_invested': Decimal('0'),
            }

        portfolio_dict[symbol]['balance'] += dep.coin_quantity
        portfolio_dict[symbol]['total_invested'] += dep.amount

    portfolios = []
    total_value = Decimal('0')
    total_invested = Decimal('0')
    total_profit_loss = Decimal('0')

    for data in portfolio_dict.values():
        crypto = data['cryptocurrency']
        price = Decimal(str(crypto.current_price))  # ✅ Use str to avoid float rounding issues
        balance = data['balance']
        invested = data['total_invested']
        current_value = price * balance
        profit_loss = current_value - invested
        profit_loss_percentage = (profit_loss / invested * 100) if invested > 0 else Decimal('0')

        data.update({
            'current_price': price,
            'price_change_24h': Decimal(str(crypto.price_change_24h)),  # ✅ Add this
            'current_value': current_value,
            'profit_loss': profit_loss,
            'profit_loss_percentage': profit_loss_percentage,
        })

        portfolios.append(data)
        total_value += current_value
        total_invested += invested
        total_profit_loss += profit_loss

    total_profit_loss_percentage = (total_profit_loss / total_invested * 100) if total_invested > 0 else Decimal('0')

    context = {
        'portfolios': portfolios,
        'total_value': total_value,
        'total_invested': total_invested,
        'total_profit_loss': total_profit_loss,
        'total_profit_loss_percentage': total_profit_loss_percentage,
        'last_updated': now(),  # ✅ Fixed: Pass this for template
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
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cryptocurrencies = context['cryptocurrencies']

        # Compute stats
        total = cryptocurrencies.count()
        positive = cryptocurrencies.filter(price_change_24h__gte=0).count()
        negative = cryptocurrencies.filter(price_change_24h__lt=0).count()
        inactive = cryptocurrencies.filter(is_active=False).count()

        # Add to context
        context.update({
            'total_cryptos': total,
            'positive_change_count': positive,
            'negative_change_count': negative,
            'inactive_count': inactive,
        })
        return context

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

@require_POST
def toggle_crypto_status(request, crypto_id):
    try:
        crypto = Cryptocurrency.objects.get(pk=crypto_id)
    except Cryptocurrency.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Cryptocurrency not found'}, status=404)

    crypto.is_active = not crypto.is_active
    crypto.save()

    return JsonResponse({
        'success': True,
        'new_status': crypto.is_active,
        'message': f"{crypto.name} is now {'Active' if crypto.is_active else 'Inactive'}"
    })


class CryptocurrencyDetailView(LoginRequiredMixin, UserPassesTestMixin, DetailView):
    model = Cryptocurrency
    template_name = 'trading/admin/crypto_detail.html'
    context_object_name = 'crypto'

    def test_func(self):
        return self.request.user.is_staff
