from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Event
from .forms import EventForm
from django.db.models import Count, Sum
from datetime import datetime


def home(request):
    # Самые популярные мероприятия (по количеству заказов)
    popular_events = Event.objects.annotate(
        orders_count=Count('order')
    ).filter(
        orders_count__gt=0
    ).order_by('-orders_count')[:6]
    
    # Если нет популярных, показываем предстоящие
    if not popular_events:
        popular_events = Event.objects.filter(
            event_date__gte=datetime.now()
        ).order_by('event_date')[:6]
    
    # Если и предстоящих нет, показываем последние добавленные
    if not popular_events:
        popular_events = Event.objects.all().order_by('-created_at')[:6]
    
    return render(
        request,
        'events/home.html',
        {'events': popular_events}
    )


def event_list(request):
    events = Event.objects.all()
    return render(request, 'events/event_list.html', {'events': events})


def event_detail(request, pk):
    event = get_object_or_404(Event, pk=pk)
    is_favorite = False
    
    if request.user.is_authenticated:
        is_favorite = event.favorites.filter(id=request.user.id).exists()
    
    return render(
        request,
        'events/event_detail.html',
        {
            'event': event,
            'is_favorite': is_favorite
        }
    )


@login_required
def toggle_favorite(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if event.favorites.filter(id=request.user.id).exists():
        event.favorites.remove(request.user)
        messages.info(request, f'Мероприятие "{event.title}" удалено из избранного')
    else:
        event.favorites.add(request.user)
        messages.success(request, f'Мероприятие "{event.title}" добавлено в избранное')
    
    return redirect('event_detail', pk=event.id)


@login_required
def favorite_events(request):
    favorite_events = request.user.favorite_events.all()
    return render(
        request,
        'events/favorite_events.html',
        {'favorite_events': favorite_events}
    )


def search_events(request):
    query = request.GET.get('q')
    if query:
        events = Event.objects.filter(title__icontains=query)
    else:
        events = Event.objects.all()
    
    return render(request, 'events/event_list.html', {'events': events})


@login_required
def create_event(request):
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = EventForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('event_list')
    else:
        form = EventForm()
    
    return render(request, 'events/event_create.html', {'form': form})


@login_required
def update_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    
    if request.method == 'POST':
        if 'remove_image' in request.POST:
            if event.image:
                event.image.delete(save=False)
                event.image = None
        
        form = EventForm(request.POST, request.FILES, instance=event)
        if form.is_valid():
            form.save()
            return redirect('event_detail', pk=event.id)
    else:
        form = EventForm(instance=event)
    
    return render(request, 'events/event_edit.html', {'form': form, 'event': event})


@login_required
def delete_event(request, pk):
    event = get_object_or_404(Event, pk=pk)
    event.delete()
    return redirect('event_list')