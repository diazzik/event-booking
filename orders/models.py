from django.db import models
from users.models import User
from events.models import Event

class Order(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Ожидает'),
        ('paid', 'Оплачен'),
        ('cancelled', 'Отменён'),
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE
    )

    event = models.ForeignKey(
        Event,
        on_delete=models.CASCADE
    )

    ticket_count = models.IntegerField()

    total_price = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )