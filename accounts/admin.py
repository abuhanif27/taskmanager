from django.contrib import admin
from .models import CustomUser

# Register your models here.

CustomUser._meta.verbose_name = 'User'
CustomUser._meta.verbose_name_plural = 'Users'


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
	list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_active')
	list_filter = ('is_staff', 'is_active', 'is_superuser')
	search_fields = ('email', 'first_name', 'last_name')
	ordering = ('email',)
