from django.urls import path
from .views import RegisterAPIView, LoginAPIView, GetHotelDataAPIView, RoomBookingAPIView

urlpatterns = [
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('get-hotel-data/',GetHotelDataAPIView.as_view(), name='get-hotel-data'),
    path('bookingroom/', RoomBookingAPIView.as_view(), name='bookingroom'),
]

