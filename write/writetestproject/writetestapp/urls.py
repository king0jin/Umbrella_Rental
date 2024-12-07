from django.urls import path
from .views import helloAPI, userAPI, umbrellaAPI, reservationsAPI, reservationStatusAPI, cancelReservationAPI

urlpatterns = [
    path("hello/", helloAPI), #서버 연결 test용 요청
    path("user/", userAPI), #유저 등록 요청
    path("umbrella/", umbrellaAPI), #우산 대여 예약 요청
    path("reservations/", reservationsAPI), #대여 예약 정보 기록 요청
    path("reservations/<int:reservation_id>/status/", reservationStatusAPI),
    path("reservations/<int:reservation_id>/cancel/", cancelReservationAPI),
]
# from rest_framework.routers import DefaultRouter
# from .views import UserViewSet, UmbrellaViewSet, ReservationViewSet

# router = DefaultRouter()
# router.register(r'users', UserViewSet, basename='user')
# router.register(r'umbrellas', UmbrellaViewSet, basename='umbrella')
# router.register(r'reservations', ReservationViewSet, basename='reservation')

# urlpatterns = router.urls