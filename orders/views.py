from django.shortcuts import redirect, render, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import Order
from events.models import Event


@login_required
def book_ticket(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    
    if request.method == 'POST':
        count = int(request.POST.get('ticket_count', 1))
        
        if count <= event.available_tickets:
            total_price = event.price * count

            Order.objects.create(
                user=request.user,
                event=event,
                ticket_count=count,
                total_price=total_price,
                status='paid' 
            )

            event.available_tickets -= count
            event.save()
            
            messages.success(request, f'Билеты успешно приобретены! Сумма: {total_price} ₽')
            return redirect('order_success')
        else:
            messages.error(request, 'Недостаточно билетов!')
    
    return redirect('event_detail', pk=event.id)


@login_required
def my_orders(request):
    orders = Order.objects.filter(
        user=request.user
    ).order_by('-created_at')
    
    total_spent = sum(order.total_price for order in orders)
    
    return render(
        request,
        'orders/my_orders.html',
        {
            'orders': orders,
            'total_spent': total_spent,
        }
    )


@login_required
def cancel_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    
    if order.status == 'paid':
        order.status = 'cancelled'
        order.save()
        messages.info(request, f'Заказ #{order.id} отменён')
    
    return redirect('my_orders')


@login_required
def order_success(request):
    return render(request, 'orders/order_success.html')