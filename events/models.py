from django.db import models
from django.conf import settings

class Event(models.Model):
    CATEGORY_CHOICES = (
        ('concert', 'Концерт'),
        ('theatre', 'Театр'),
        ('festival', 'Фестиваль'),
        ('exhibition', 'Выставка'),
    )
    
    title = models.CharField(max_length=255)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    total_tickets = models.IntegerField()
    available_tickets = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    favorites = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='favorite_events',
        blank=True
    )
    
    def __str__(self):
        return self.title