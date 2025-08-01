from django.contrib import admin
from users import models as users_models


@admin.register(users_models.CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = (
        "first_name",
        "last_name",
        "email",
        "date_joined",
        "is_staff",
        "is_superuser",
    )
    list_filter = ("date_joined",)

    def save_model(self, request, obj, form, change):
        if obj.pk is None:
            obj.set_password(obj.password)
        super().save_model(request, obj, form, change)
