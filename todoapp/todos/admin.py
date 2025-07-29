from django.contrib import admin

from todos.models import Todo

@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):
    list_display = ("user", "name", "done", "date_created" , "date_completed")
    list_filter = ("done", "date_created")
