from django.contrib import admin
from Users.models import UserModel, Hotel, TemporaryBusyroomsModel, TgUsersModel


# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('name', 'email')

class TgADmin(admin.ModelAdmin):
    list_display = ('name', 'user_id')

admin.site.register(UserModel, UserAdmin)
admin.site.register(Hotel)
admin.site.register(TemporaryBusyroomsModel)
admin.site.register(TgUsersModel,TgADmin)