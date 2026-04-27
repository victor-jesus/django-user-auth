from django.contrib import admin
from .models import Task

class TaskAdmin(Task):
    list_display = ('id', 'title', 'user', 'status', 'created_at')
    list_filter = ('status', 'user')
    search_fields = ('title',)
