from sys import maxsize

from django.db import models

class UserModel(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Hotel(models.Model):
    hotel_name = models.CharField(max_length=255)
    hotel_location = models.CharField(max_length=255)
    price_night_in_dollar = models.DecimalField(max_digits=10, decimal_places=2)
    available_rooms = models.IntegerField()
    longitude = models.CharField(max_length=32, null=True)
    latitude = models.CharField(max_length=32, null=True)
    images_1 = models.ImageField(upload_to='hotel_images/', null=True, blank=True)
    images_2 = models.ImageField(upload_to='hotel_images/', null=True, blank=True)
    images_3 = models.ImageField(upload_to='hotel_images/', null=True, blank=True)

    def __str__(self):
        return self.hotel_name

class TgUsersModel(models.Model):
    name = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    user_id = models.IntegerField()
    def __str__(self):
        return f'{self.user_id}, {self.name}'



class TemporaryBusyroomsModel(models.Model):
    user = models.ForeignKey(UserModel, on_delete=models.CASCADE)
    hotel = models.ForeignKey(Hotel, on_delete=models.CASCADE)
    room_number = models.CharField(max_length=50)
    check_in = models.DateTimeField()
    check_out = models.DateTimeField()
    booking_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.name} {self.hotel.hotel_name} {self.room_number}"

    class Meta:
        unique_together = ('user', 'hotel', 'room_number', 'check_in', 'check_out')

