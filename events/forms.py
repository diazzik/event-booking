from django import forms
from .models import Event


class EventForm(forms.ModelForm):

    class Meta:
        model = Event

        fields = [
            'title',
            'description',
            'category',
            'event_date',
            'location',
            'total_tickets',
            'available_tickets',
            'price',
            'image'
        ]

        widgets = {
            'event_date': forms.DateTimeInput(
                attrs={'type': 'datetime-local'}
            )
        }