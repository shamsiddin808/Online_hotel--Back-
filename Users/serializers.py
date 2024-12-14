from rest_framework import serializers
from .models import UserModel, Hotel, TemporaryBusyroomsModel, TgUsersModel


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


class PricingRoomsSerializer(serializers.ModelSerializer):
    class Meta:
        model = TemporaryBusyroomsModel
        fields = 'hotel', 'check_in', 'check_out'


