from typing import Iterable, Optional
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.dispatch import receiver
from django.db.models.signals import post_save
from guardian.shortcuts import assign_perm
from django.contrib.auth.models import Group
from django.utils import timezone

from user.models import MyUser

# Create your models here.


class CategoryNameField(models.CharField):

    def get_prep_value(self, value):
        return str(value).lower()


class HandleMaterialField(models.CharField):

    def get_prep_value(self, value):
        return str(value).lower()


class ProdNameField(models.CharField):

    def get_prep_value(self, value):
        return str(value).lower()


class Category(models.Model):
    add_by = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, verbose_name=_('Creado por'),)
    name = CategoryNameField(
        max_length=70, verbose_name=_('Categoria'), unique=True)
    description = models.TextField(
        max_length=450, verbose_name=_('Descripción'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = _("Categorias")
        permissions = [
            ('staff_add_category', 'OLP staff add category'),
            ('staff_view_category', 'OLP staff view category'),
            ('staff_change_category', 'OLP staff change category'),
            ('staff_delete_category', 'OLP staff delete category'),
        ]

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Handle(models.Model):
    add_by = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, verbose_name=_("Agregado por"))
    material = HandleMaterialField(
        max_length=100, verbose_name=_("Material"), unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = _("Empuñaduras")
        permissions = [
            ('staff_add_handle', 'OLP staff add handle'),
            ('staff_view_handle', 'OLP staff view handle'),
            ('staff_change_handle', 'OLP staff change handle'),
            ('staff_delete_handle', 'OLP staff delete handle'),
        ]

    def save(self, *args, **kwargs):
        self.material = self.material.lower()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.material


class Product(models.Model):
    add_by = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, verbose_name=_("Creado por"))
    name = ProdNameField(max_length=100, unique=True,
                         verbose_name=_("Producto"))
    description = models.TextField(
        max_length=400, verbose_name=_("Descrispción"))
    img_primary = models.ImageField(
        upload_to='images/product', verbose_name=_("Imagen principal"))
    price = models.DecimalField(
        max_digits=8, decimal_places=2, verbose_name=_("Precio"))

    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True, verbose_name=_("Categoria"))
    blade_size = models.CharField(
        max_length=50, default='__ x __ x __ mm', verbose_name=_("Tamaño de la hoja en mm"))
    blade_material = models.CharField(
        max_length=50, null=True, blank=True, verbose_name=_("Material de la hoja"))
    handle = models.ForeignKey(
        Handle, on_delete=models.SET_NULL, null=True, verbose_name=_("Empuñadura"))
    handle_size = models.CharField(
        max_length=50, default='__ x __ x __ mm', verbose_name=_("Tamaño de la empuñadura en mm"))

    quantity = models.PositiveIntegerField(
        default=1, verbose_name=_("Cantidad"))
    stock = models.BooleanField(default=True,  verbose_name=_("Hay Stock"))

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publish_date = models.DateTimeField(default=timezone.now())

    def save(self, *args, **kwargs):
        self.name = self.name.lower()
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name

    class Meta:
        ordering = ['-updated_at']
        verbose_name_plural = "Productos"
        permissions = [
            ('staff_add_product', 'OLP staff add product'),
            ('staff_view_product', 'OLP staff view product'),
            ('staff_change_product', 'OLP staff change product'),
            ('staff_delete_product', 'OLP staff delete product'),
        ]


class Prod_SecImg(models.Model):
    img_sec_1 = models.ImageField(upload_to='images/prod-sec')
    img_sec_2 = models.ImageField(upload_to='images/prod-sec')
    img_sec_3 = models.ImageField(upload_to='images/prod-sec')
    img_sec_4 = models.ImageField(upload_to='images/prod-sec', null=True)
    img_sec_5 = models.ImageField(upload_to='images/prod-sec', null=True)
    prod = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = "Imagenes Secundarias de Productos"
        permissions = [
            ('staff_add_prod_secimg', 'OLP staff add prod_secimg'),
            ('staff_view_prod_secimg', 'OLP staff view prod_secimg'),
            ('staff_change_prod_secimg', 'OLP staff change prod_secimg'),
            ('staff_delete_prod_secimg', 'OLP staff delete prod_secimg'),
        ]


class Message(models.Model):
    user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, verbose_name=_("Creado por"))
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='comments', verbose_name=_("Producto correspondiente"))
    body = models.TextField(max_length=512, verbose_name=_("Comentario"))

    have_answered = models.BooleanField(
        verbose_name=_("Fue respondido?"), default=False)

    staff_user = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, null=True, related_name='awnser_staff_user', verbose_name=_("Staff que respondio"))
    answer = models.TextField(
        max_length=512, null=True, verbose_name=_("Respuesta"))
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Comentarios"
        permissions = [
            ('staff_add_message', 'OLP staff add message'),
            ('staff_view_message', 'OLP staff view message'),
            ('staff_change_message', 'OLP staff change message'),
            ('staff_delete_message', 'OLP staff delete message'),
        ]


class Cart(models.Model):
    owner = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    items = models.ManyToManyField(
        Product, related_name="carts", through='CartItems')

    class Meta:
        verbose_name_plural = "Carrito"

    def clear_cart(self):
        self.items.clear()


class BaseItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    class Meta:
        abstract = True


class CartItems(BaseItem):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    add_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['product', 'cart'], name='unique_product_cart')]
        verbose_name_plural = "Producto en el carrito"

    def __str__(self):
        return self.product.name


@receiver(post_save, sender=Category)
def user_post_save(sender, instance, **kwargs):
    staff_group, created = Group.objects.get_or_create(name='Staff')

    assign_perm('staff_view_category', staff_group, instance)

    assign_perm('staff_view_category', instance.add_by, instance)
    assign_perm('staff_change_category', instance.add_by, instance)
    assign_perm('staff_delete_category', instance.add_by, instance)


@receiver(post_save, sender=Handle)
def user_post_save(sender, instance, **kwargs):
    staff_group, created = Group.objects.get_or_create(name='Staff')

    assign_perm('staff_view_handle', staff_group, instance)

    assign_perm('staff_view_handle', instance.add_by, instance)
    assign_perm('staff_change_handle', instance.add_by, instance)
    assign_perm('staff_delete_handle', instance.add_by, instance)


@receiver(post_save, sender=Product)
def user_post_save(sender, instance, **kwargs):
    staff_group, created = Group.objects.get_or_create(name='Staff')

    assign_perm('staff_view_product', staff_group, instance)

    assign_perm('staff_view_product', instance.add_by, instance)
    assign_perm('staff_change_product', instance.add_by, instance)
    assign_perm('staff_delete_product', instance.add_by, instance)


@receiver(post_save, sender=Prod_SecImg)
def user_post_save(sender, instance, **kwargs):
    staff_group, created = Group.objects.get_or_create(name='Staff')

    assign_perm('staff_view_prod_secimg', staff_group, instance)

    assign_perm('staff_view_prod_secimg', instance.prod.add_by, instance)
    assign_perm('staff_change_prod_secimg', instance.prod.add_by, instance)
    assign_perm('staff_delete_prod_secimg', instance.prod.add_by, instance)


@receiver(post_save, sender=Message)
def user_post_save(sender, instance, **kwargs):
    staff_group, created = Group.objects.get_or_create(name='Staff')

    assign_perm('staff_view_message', staff_group, instance)

    assign_perm('staff_view_message', instance.user, instance)
    assign_perm('staff_change_message', instance.user, instance)
    assign_perm('staff_delete_message', instance.user, instance)
