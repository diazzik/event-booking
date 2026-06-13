from django.urls import path
from . import views

urlpatterns = [
    path('', views.admin_dashboard, name='admin_dashboard'),
    path('events/', views.admin_events, name='admin_events'),
    path('users/', views.admin_users, name='admin_users'),
    path('orders/', views.admin_orders, name='admin_orders'),
    path('statistics/', views.statistics, name='statistics'),
    path('categories/', views.admin_categories, name='admin_categories'),
    path('settings/', views.admin_settings, name='admin_settings'),
]