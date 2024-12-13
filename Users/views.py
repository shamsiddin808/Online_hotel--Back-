from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate
from django.core.mail import send_mail


from .models import UserModel, Hotel, TemporaryBusyroomsModel
from .serializers import UserSerializer, UserLoginSerializer, HotelSerializer, RoomSerializer


class RegisterAPIView(APIView):
    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Royxatdan otdingiz'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginAPIView(APIView):
    @swagger_auto_schema(request_body=UserLoginSerializer)
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        if not email or not password:
            return Response({'HATO': 'Email parolni kiritish shart'}, status=400)
        user = UserModel.objects.filter(email=email).first()
        if not user:
            return Response({'HATO': 'User not found'}, status=400)
        else:
            if password != user.password:
                return Response({'HATO': 'Parol Xato'}, status=400)
            elif password == user.password:
                return Response({'HATO': f'Siz akkauntga kirdingiz {user.name}'}, status=200)


class GetHotelDataAPIView(APIView):
    def get(self, request):
        hotels = Hotel.objects.all()
        hotel_data = HotelSerializer(hotels, many=True).data
        return Response({"message": hotel_data}, status=200)



from datetime import datetime

class RoomBookingAPIView(APIView):
    @swagger_auto_schema(request_body=RoomSerializer)
    def post(self, request):
        user_id = request.data.get('user')
        user = UserModel.objects.filter(id=user_id).first()
        hotel_id = request.data.get('hotel')
        room_number = request.data.get('room_number')
        check_in = request.data.get('check_in')
        check_out = request.data.get('check_out')
        hotel_name = Hotel.objects.filter(id=hotel_id).first()
        try:
            pass
        except hotel_name.DoesNotExist:
            return Response({'HATO': 'Mehmonhona mavjud emas'}, status=400)


        bookings = TemporaryBusyroomsModel.objects.filter(hotel=hotel_name, room_number=room_number, check_in__lt=check_out, check_out__gt=check_in)

        if bookings.exists():
            return Response({"message": "bu hona band"}, status=400)

        serializer = RoomSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user, hotel=hotel_name)
            return Response({"message": "Hona muvofaqiyatli band qildik"}, status=201)
        return Response(serializer.errors, status=400)


class SendEmailView(APIView):
    def post(self, request):
        recipient_email = request.data.get("email")  # Kimga yuborishni olish
        verification_code = "123456"  # Bu yerda kod yaratishingiz mumkin

        # Email jo'natish
        subject = "Tasdiqlash Kodi"
        message = f"Sizning tasdiqlash kodingiz: {verification_code}"
        from_email = "ultrateam050@gmail.com"
        recipient_list = [recipient_email]

        try:
            send_mail(subject, message, from_email, recipient_list)
            return Response({"success": "Kod muvaffaqiyatli yuborildi!"}, status=200)
        except Exception as e:
            return Response({"error": str(e)}, status=400)