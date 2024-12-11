from rest_framework import serializers
from .models import UserModel, Hotel, TemporaryBusyroomsModel


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = '__all__'

class UserLoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserModel
        fields = 'email', 'password'

class HotelSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hotel
        fields = '__all__'





class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryBusyroomsModel
        fields = '__all__'