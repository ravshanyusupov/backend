from django.contrib import admin

from django.contrib.auth.admin import AdminPasswordChangeForm, UserAdmin
from src.apps.users.models import User
from src.apps.users.forms import UserChangeForm, UserCreationForm


class CustomUserAdmin(UserAdmin):
    fieldsets = (
        (
            None,
            {
                "fields": (
                    "username",
                    "password",
                    "district",
                    "region",
                    "user_type",
                )
            },
        ),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_superuser",
                    "user_permissions",
                    "groups",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "created_at")}),
    )
    limited_fieldset = (
        (None, {"fields": ("username",)}),
        ("Important dates", {"fields": ("last_login", "created_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "username",
                    "password1",
                    "password2",
                    "region",
                    "district",
                    "user_type",
                ),
            },
        ),
    )

    form = UserChangeForm
    add_form = UserCreationForm
    change_password_form = AdminPasswordChangeForm

    list_display = ("id", "username", "is_superuser")
    list_filter = ("is_staff", "is_superuser", "is_active", "groups")
    search_fields = ("username",)
    ordering = ("username",)
    readonly_fields = ("last_login", "created_at")


admin.site.register(User, CustomUserAdmin)
