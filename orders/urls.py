from django.urls import path
from . import views

urlpatterns = [

    path(
        'book/<int:event_id>/',
        views.book_ticket,
        name='book_ticket'
    ),

    path(
        'my-orders/',
        views.my_orders,
        name='my_orders'
    ),

    path(
        'cancel/<int:order_id>/',
        views.cancel_order,
        name='cancel_order'
    ),

    path(
        'success/',
        views.order_success,
        name='order_success'
    ),
]