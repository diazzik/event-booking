from django.contrib import admin
from .models import Event


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):

    list_display = (
        'title',
        'category',
        'event_date',
        'price',
        'available_tickets'
    )

    search_fields = (
        'title',
        'location'
    )

    list_filter = (
        'category',
        'event_date'
    )