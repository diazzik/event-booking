from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required
from django.db.models import Sum, Count, Q, F, FloatField
from django.db.models.functions import Coalesce
from datetime import datetime

from events.models import Event
from orders.models import Order
from users.models import User


@staff_member_required
def admin_dashboard(request):
    events_count = Event.objects.count()
    users_count = User.objects.count()
    orders_count = Order.objects.count()
    
    return render(
        request,
        'dashboard/index.html',
        {
            'events_count': events_count,
            'users_count': users_count,
            'orders_count': orders_count
        }
    )


@staff_member_required
def admin_events(request):
    events = Event.objects.all()
    return render(
        request,
        'dashboard/admin_events.html',
        {'events': events}
    )


@staff_member_required
def admin_users(request):
    users = User.objects.all()
    return render(
        request,
        'dashboard/admin_users.html',
        {'users': users}
    )


# @staff_member_required
# def admin_orders(request):
#     orders = Order.objects.all()
#     return render(
#         request,
#         'dashboard/admin_orders.html',
#         {'orders': orders}
#     )

@staff_member_required
def admin_orders(request):
    orders = Order.objects.all().order_by('-created_at')
    return render(
        request,
        'dashboard/admin_orders.html',
        {'orders': orders}
    )

@staff_member_required
def statistics(request):
    # Общая статистика
    total_orders = Order.objects.count()
    total_users = User.objects.count()
    
    # Простой подсчёт дохода через Python
    paid_orders = Order.objects.filter(status='paid')
    total_income = sum(order.total_price for order in paid_orders) if paid_orders else 0
    
    # Статистика по каждому мероприятию
    event_stats = []
    events = Event.objects.all()
    
    for event in events:
        # Количество проданных билетов
        sold_orders = Order.objects.filter(event=event, status='paid')
        sold_tickets = sum(order.ticket_count for order in sold_orders)
        total_revenue = sum(order.total_price for order in sold_orders)
        
        # Процент заполняемости
        if event.total_tickets > 0:
            occupancy = round((sold_tickets * 100.0) / event.total_tickets, 1)
        else:
            occupancy = 0
        
        if sold_tickets > 0:
            event_stats.append({
                'id': event.id,
                'title': event.title,
                'event_date': event.event_date,
                'total_tickets': event.total_tickets,
                'sold_tickets': sold_tickets,
                'total_revenue': total_revenue,
                'occupancy': occupancy,
            })
    
    event_stats.sort(key=lambda x: x['occupancy'], reverse=True)
    top_events = event_stats[:3]
    
    upcoming_events = []
    future_events = Event.objects.filter(
        event_date__gte=datetime.now(),
        available_tickets__gt=0
    )
    
    for event in future_events:
        sold = sum(order.ticket_count for order in Order.objects.filter(event=event, status='paid'))
        
        if event.total_tickets > 0:
            predicted = min(round(((sold + 50) * 100.0) / event.total_tickets, 1), 100)
        else:
            predicted = 0
        
        upcoming_events.append({
            'id': event.id,
            'title': event.title,
            'event_date': event.event_date,
            'available_tickets': event.available_tickets,
            'occupancy_prediction': predicted,
        })
    
    upcoming_events.sort(key=lambda x: x['occupancy_prediction'], reverse=True)
    upcoming_events = upcoming_events[:5]
    
    return render(
        request,
        'dashboard/statistics.html',
        {
            'total_orders': total_orders,
            'total_users': total_users,
            'total_income': total_income,
            'event_stats': event_stats,
            'top_events': top_events,
            'upcoming_events': upcoming_events,
        }
    )


@staff_member_required
def admin_categories(request):
    """Управление категориями мероприятий"""
    from events.models import Event
    
    # Получаем список всех категорий с количеством мероприятий
    categories = []
    category_choices = Event.CATEGORY_CHOICES
    
    for code, name in category_choices:
        count = Event.objects.filter(category=code).count()
        categories.append({
            'code': code,
            'name': name,
            'count': count,
        })
    
    return render(
        request,
        'dashboard/admin_categories.html',
        {'categories': categories}
    )


@staff_member_required
def admin_settings(request):
    """Настройки системы"""
    from django.conf import settings
    
    context = {
        'site_name': 'EventHub',
        'debug_mode': settings.DEBUG,
        'timezone': settings.TIME_ZONE,
        'language': settings.LANGUAGE_CODE,
    }
    
    return render(
        request,
        'dashboard/admin_settings.html',
        context
    )