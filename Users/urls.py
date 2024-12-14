from django.urls import path
from setuptools.extern import names

from .views import RegisterUserView, LoginAPIView, GetHotelDataAPIView, RoomBookingAPIView, SendEmailView, GetUserData, \
    GetUserDataTgView, RegisterAPIView, PricingRoomAPIView, GetOneHoteldataView

urlpatterns = [
    path('register-telegram/', RegisterUserView.as_view(), name='register-mobile'),
    path('register/', RegisterAPIView.as_view(), name='register'),
    path('login/', LoginAPIView.as_view(), name='login'),
    path('get-hotel-data/',GetHotelDataAPIView.as_view(), name='get-hotel-data'),
    path('bookingroom/', RoomBookingAPIView.as_view(), name='bookingroom'),
    path('send-email/', SendEmailView.as_view(), name='send-email'),
    path('get-user/<str:email>/', GetUserData.as_view(), name='get-user'),
    path('get-tg-user/<int:user_id>/', GetUserDataTgView.as_view(), name='get-tg-user'),
    path('pricinghotel/',  PricingRoomAPIView.as_view(), name='pricinghotel'),
    path('get-one-hotel/<int:hotel_id>/', GetOneHoteldataView.as_view(), name='get-one-hotel'),
]

