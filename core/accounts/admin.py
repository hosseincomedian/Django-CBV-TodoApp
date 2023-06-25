from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from accounts.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    model = User
    list_display = (
        "email",
        "is_staff",
        "is_active",
        "is_verified",
    )
    list_filter = (
        "email",
        "is_staff",
        "is_active",
    )
    search_fields = ("email",)
    ordering = ("email",)
    fieldsets = (
        ("Authentication", {"fields": ("email", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_active",
                    "is_verified",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        (
            "important dates",
            {
                "fields": ("last_login",),
            },
        ),
    )

    add_fieldsets = (
        (
            "none",
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
    )
