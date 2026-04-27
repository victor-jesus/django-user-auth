from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User

    list_display = ('id', 'username', 'email', 'is_staff', 'is_active')
    list_filter = ('is_staff', 'is_active')

    search_fields = ('username', 'email')
    ordering = ('id',)

    fieldsets = UserAdmin.fieldsets + (
        ("Informações adicionais", {
            "fields": ()
        }),
    )
    
admin.site.site_header = "Painel do Todo"
admin.site.site_title = "Admin Todo"
admin.site.index_title = "Administração"