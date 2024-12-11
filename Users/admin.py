from django.contrib import admin
from Users.models import UserModel, Hotel, TemporaryBusyroomsModel


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

admin.site.register(UserModel, UserAdmin)
admin.site.register(Hotel)
admin.site.register(TemporaryBusyroomsModel)