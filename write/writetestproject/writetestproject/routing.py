from django.urls import path
from writetestapp.consumers import UmbrellaReservationConsumer

websocket_urlpatterns = [
    path('ws/reservation/', UmbrellaReservationConsumer.as_asgi()),
]
