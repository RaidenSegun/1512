from django.contrib import admin
from .models import User, Todo
from apps.todo.forms import TodoForm



class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'phone_number', 'created_at', 'age')
    search_fields = ('username', 'email', 'phone_number')
    list_filter = ('created_at',)
    ordering = ('created_at',)


class TodoAdmin(admin.ModelAdmin):
    form = TodoForm
    list_display = ('title', 'is_completed', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('is_completed', 'created_at')
    ordering = ('created_at',)


admin.site.register(User, UserAdmin)
admin.site.register(Todo, TodoAdmin)