from django.contrib import admin
from users.models import CustomUser

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("first_name", "last_name", "email", "date_joined" , "is_staff" , "is_superuser")
    list_filter = ("date_joined",) 
