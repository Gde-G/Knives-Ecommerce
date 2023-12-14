from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.core.exceptions import ValidationError
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField

import random


def get_profile_image_upload_path(self, filename):
    # Generate a unique path for the user's profile image
    return f'users/profile_img/{self.username}/{filename}'


class MyUserManager(BaseUserManager):
    def create_user(self, username, email, password, **other_field):
        if not username:
            raise ValueError(_("You must provide a username "))
        if not email:
            raise ValueError(_("You must provide a email "))
        if not password:
            raise ValueError(_("You must provide a password"))

        email = self.normalize_email(email)

        user = self.model(
            username=username,
            email=email,
            **other_field
        )

        user.set_password(password)
        user.save()

        return user

    def create_staff(self, username, email, password, **other_field):
        other_field.setdefault('is_staff', True)
        other_field.setdefault('is_superuser', False)
        other_field.setdefault('is_active', False)

        if other_field.get('is_staff') is not True:
            raise ValidationError(_('Restricted Access'))

        return self.create_user(username, email, password, **other_field)

    def create_superuser(self, username, email, password, **other_field):
        other_field.setdefault('is_staff', True)
        other_field.setdefault('is_superuser', True)
        other_field.setdefault('is_active', True)

        if other_field.get('is_staff') is not True:
            raise ValidationError(_('Restricted Access'))
        if other_field.get('is_superuser') is not True:
            raise ValidationError(_('Restricted Access'))

        return self.create_user(username, email, password, **other_field)

    def find_by_email(self, email):
        try:
            return self.get(email=email)
        except self.model.DoesNotExist:
            return None

    def find_by_username(self, username):
        try:
            return self.get(username=username)
        except self.model.DoesNotExist:
            return None


class MyUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
        unique=True, verbose_name=_("Correo electronico"))
    username = models.CharField(
        unique=True, max_length=150, verbose_name=_("Nombre de Usuario"))
    profile_img = models.ImageField(
        upload_to=get_profile_image_upload_path, null=True, blank=True, max_length=150, verbose_name=_("Imagen de perfil"))
    phone_number = PhoneNumberField(
        null=True, blank=True, verbose_name=_("Numero telefonico"))
    first_name = models.CharField(
        max_length=150, null=True, blank=True, verbose_name=_("Nombre"))
    last_name = models.CharField(
        max_length=150, null=True, blank=True, verbose_name=_("Apellido"))
    birth_date = models.DateField(
        null=True, blank=True, verbose_name=_("Fecha de nacimiento"))
    country = models.ForeignKey(
        'cities_light.country', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("País"))
    region = models.ForeignKey(
        'cities_light.region', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Region / Estado"))
    city = models.ForeignKey(
        'cities_light.city', on_delete=models.CASCADE, null=True, blank=True, verbose_name=_("Ciudad"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_login = models.DateTimeField(null=True, blank=True)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = MyUserManager()

    USERNAME_FIELD = 'username'

    EMAIL_FIELD = 'email'

    REQUIRED_FIELDS = ['email']

    class Meta:
        verbose_name_plural = _("Usuarios")

    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"

    def get_short_name(self):
        return self.first_name

    def __str__(self):
        return self.username

    def save(self, *args, **kwargs):
        if not self.profile_img:
            # List of available default profile images
            default_images = ['default-profile-pic-blue.png',
                              'default-profile-pic-red.png', 'default-profile-pic-green.png']
            random_image = random.choice(default_images)

            # Get the URL path of the selected default profile image
            default_image_path = f'users/profile_img/{random_image}'

            # Set the profile_img field to the selected default image URL
            self.profile_img = default_image_path

        super().save(*args, **kwargs)
