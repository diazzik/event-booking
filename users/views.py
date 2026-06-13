from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import update_session_auth_hash
from django.contrib import messages
from django.http import JsonResponse
from django.db import models
from .forms import RegisterForm, ProfileForm, UserSettingsForm, ChangePasswordForm
from orders.models import Order
from events.models import Event


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegisterForm()
    
    return render(request, 'users/register.html', {'form': form})


@login_required
def profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    
    # Статистика пользователя
    orders_count = Order.objects.filter(user=request.user).count()
    favorites_count = request.user.favorites.count()
    total_spent = Order.objects.filter(user=request.user, status='paid').aggregate(models.Sum('total_price'))['total_price__sum'] or 0
    
    return render(
        request,
        'users/profile.html',
        {
            'form': form,
            'orders_count': orders_count,
            'favorites_count': favorites_count,
            'total_spent': total_spent,
        }
    )


@login_required
def my_orders(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    
    return render(
        request,
        'users/my_orders.html',
        {'orders': orders}
    )


@login_required
def favorites(request):
    favorites = request.user.favorites.all()
    
    return render(
        request,
        'users/favorites.html',
        {'favorites': favorites}
    )


@login_required
def add_to_favorites(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    request.user.favorites.add(event)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'added', 'message': 'Мероприятие добавлено в избранное'})
    
    messages.success(request, f'Мероприятие "{event.title}" добавлено в избранное')
    return redirect('event_detail', pk=event_id)


@login_required
def remove_from_favorites(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    request.user.favorites.remove(event)
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'status': 'removed', 'message': 'Мероприятие удалено из избранного'})
    
    messages.success(request, f'Мероприятие "{event.title}" удалено из избранного')
    return redirect('favorites')


@login_required
def settings_view(request):
    if request.method == 'POST':
        form = UserSettingsForm(request.POST, instance=request.user)
        password_form = ChangePasswordForm(request.POST)
        
        if 'update_profile' in request.POST:
            if form.is_valid():
                form.save()
                messages.success(request, 'Настройки профиля обновлены!')
                return redirect('settings')
        
        elif 'change_password' in request.POST:
            if password_form.is_valid():
                old_password = password_form.cleaned_data['old_password']
                new_password1 = password_form.cleaned_data['new_password1']
                new_password2 = password_form.cleaned_data['new_password2']
                
                if not request.user.check_password(old_password):
                    messages.error(request, 'Неверный старый пароль')
                elif new_password1 != new_password2:
                    messages.error(request, 'Новые пароли не совпадают')
                else:
                    request.user.set_password(new_password1)
                    request.user.save()
                    update_session_auth_hash(request, request.user)
                    messages.success(request, 'Пароль успешно изменён!')
                return redirect('settings')
    else:
        form = UserSettingsForm(instance=request.user)
        password_form = ChangePasswordForm()
    
    return render(
        request,
        'users/settings.html',
        {
            'form': form,
            'password_form': password_form,
        }
    )


@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Профиль успешно обновлён!')
            return redirect('profile')
    else:
        form = ProfileForm(instance=request.user)
    
    return render(
        request,
        'users/edit_profile.html',
        {'form': form}
    )