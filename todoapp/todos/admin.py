from django.contrib import admin

from todos import models as todos_models


@admin.register(todos_models.Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "done", "date_created", "date_completed")
    list_filter = ("done", "date_created")
