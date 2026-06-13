from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('my-orders/', views.my_orders, name='my_orders'),
    path('favorites/', views.favorites, name='favorites'),
    path('favorites/add/<int:event_id>/', views.add_to_favorites, name='add_to_favorites'),
    path('favorites/remove/<int:event_id>/', views.remove_from_favorites, name='remove_from_favorites'),
    path('settings/', views.settings_view, name='settings'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
]