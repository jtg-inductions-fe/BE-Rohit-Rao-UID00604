from django.contrib import admin

class ProjectAdmin:
    list_display = ("name", "member", "max_number", "status")
    list_filter = ("max_number", "status")