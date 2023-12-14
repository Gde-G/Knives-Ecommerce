from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import MyUserCreationForm, MyUserUpdateForm
from .models import MyUser


class MyUserAdmin(UserAdmin):

    model = MyUser
    list_display = ("username", "email", "is_active",
                    "is_staff", "is_superuser")
    list_filter = ("username", "email", "is_active",
                   "is_staff", "is_superuser")
    fieldsets = (
        (None, {"fields": ("username", "email", "profile_img", "first_name", "last_name", "birth_date",
                           "country", "region", "city", "phone_number", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff",
         "is_superuser", "groups", "user_permissions")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "username", "email", "first_name", "last_name", "country", "phone_number", "password1",
                "password2", "is_active", "is_staff", "is_superuser", "groups", "user_permissions"
            )}
         ),
    )
    search_fields = ("email", "username")
    ordering = ("email", "username")


admin.site.register(MyUser, MyUserAdmin)
