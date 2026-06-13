from django.contrib import admin
from .models import Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):

    list_display = (
        'id',
        'user',
        'event',
        'ticket_count',
        'total_price',
        'status'
    )

    list_filter = (
        'status',
    )