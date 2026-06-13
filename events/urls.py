from django.urls import path
from . import views

urlpatterns = [

    path(
        '',
        views.home,
        name='home'
    ),

    path(
        'events/',
        views.event_list,
        name='event_list'
    ),

    path(
        'events/search/',
        views.search_events,
        name='search_events'
    ),

    path(
        'events/<int:pk>/',
        views.event_detail,
        name='event_detail'
    ),

    path(
        'events/create/',
        views.create_event,
        name='create_event'
    ),

    path(
        'events/<int:pk>/edit/',
        views.update_event,
        name='update_event'
    ),

    path(
        'events/<int:pk>/delete/',
        views.delete_event,
        name='delete_event'
    ),

    path('favorites/', views.favorite_events, name='favorite_events'),
    path('events/<int:pk>/favorite/', views.toggle_favorite, name='toggle_favorite'),
]