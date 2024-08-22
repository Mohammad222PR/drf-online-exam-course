from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserChangeForm, UserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ["email", "first_name", "last_name", "is_active", "role"]
    list_filter = ["is_active", "role"]
    list_per_page = 10

    fieldsets = [
        (None, {"fields": ["email", "first_name", "last_name"]}),
        ("نوع کاربر", {"fields": ["role"]}),
    ]

    add_fieldsets = [
        (None, {"fields": ["email", "first_name", "last_name", "password1", "password2"]}),
        ("نوع کاربر", {"fields": ["role"]}),
    ]

    search_fields = ["email"]
    ordering = ["email"]
    filter_horizontal = []