from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

from product.models import BaseItem, Product
from user.models import MyUser

from django.dispatch import receiver
from django.db.models.signals import post_save
from guardian.shortcuts import assign_perm
from django.contrib.auth.models import Group

import re
import hashlib
import uuid
# Create your models here.


def validate_address_num(value):
    if not re.match(r'^\d+$', value):
        raise ValidationError(
            _("'%(value)' is not a valid number."), params={"value": value})


class Address(models.Model):

    address_type_choices = [
        ('house', 'House'),
        ('apartment', 'Apartment'),
    ]

    owner = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, verbose_name=_("Usuario"))

    country = models.ForeignKey(
        'cities_light.country', on_delete=models.CASCADE, verbose_name=_("País"))
    region = models.ForeignKey(
        'cities_light.region', on_delete=models.CASCADE, verbose_name=_("Region/Estado"))
    city = models.ForeignKey(
        'cities_light.city', on_delete=models.CASCADE, verbose_name=_("Ciudad"))

    street = models.CharField(max_length=150, verbose_name=_("Calle"))
    number = models.CharField(max_length=10, validators=[
                              validate_address_num], verbose_name=_("Numero"))
    zipcode = models.CharField(max_length=10, validators=[
                               validate_address_num], verbose_name=_("Codigo postal"))

    address_type = models.CharField(
        max_length=10, choices=address_type_choices, verbose_name=_("Tipo de domicilio"))
    apartment_flor = models.CharField(
        max_length=4, null=True, blank=True, verbose_name=_("Piso del apartamento"))
    apartment_id = models.CharField(
        max_length=4, null=True, blank=True, verbose_name=_("Identificador del apartamento"))

    special_instructions = models.CharField(
        max_length=250, null=True, blank=True, verbose_name=_("Indicaciones extras"))

    choosen_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["owner", "-choosen_at"]
        verbose_name_plural = _("Direcciones")

    def __str__(self):
        return self.street + ' ' + str(self.number) + ', ' + self.region.name + ' ' + self.country.name + '.'


class Card(models.Model):
    id_type_choices = [
        ('1', 'DNI'),
        ('2', 'CPF'),
        ('3', 'SSN')
    ]
    status_choices = [
        ('approved', 'approved'),
        ('pending', 'pending'),
        ('denied', 'denied')
    ]
    issuer_choices = [
        ('visa', 'visa'),
        ('mastercard', 'mastercard'),
        ('american express', 'american express')
    ]
    type_card_choices = [
        ('credit', 'credit'),
        ('debit', 'debit')
    ]

    number = models.CharField(unique=True, max_length=24)
    expirate_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=4)
    issuer = models.CharField(max_length=20, choices=issuer_choices)
    type_card = models.CharField(max_length=7, choices=type_card_choices)
    name = models.CharField(max_length=100)
    type_id = models.CharField(max_length=4, choices=id_type_choices)
    number_id = models.CharField(max_length=20)

    last_four_digits = models.CharField(max_length=4)

    status_returned = models.CharField(max_length=10, choices=status_choices)

    class Meta:
        verbose_name_plural = "Tarjetas"

    def __str__(self):
        return self.number


class CardUser(models.Model):
    card = models.ForeignKey(Card, on_delete=models.CASCADE)
    user = models.ForeignKey(MyUser, on_delete=models.CASCADE)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-update_date']
        verbose_name_plural = "Tarjetas por usuario"


class CodeNameField(models.CharField):

    def get_prep_value(self, value):
        return str(value).lower()


class DiscountCode(models.Model):
    discount_kind_choices = [
        ('Total', 'Total'),
        ('Shipping', 'Shipping')
    ]
    add_by = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, verbose_name=_("Creado por"))
    code = CodeNameField(max_length=15, unique=True,
                         verbose_name=_("Codigo"))
    discount_kind = models.CharField(
        max_length=9, choices=discount_kind_choices)
    discount = models.IntegerField(verbose_name=_("Descuento"))
    enabled_from = models.DateField(verbose_name=_("Disponible desde"))
    enabled_to = models.DateField(verbose_name=_("Disponible hasta"))

    class Meta:
        verbose_name_plural = _("Codigo de Descuento")
        permissions = [
            ('staff_add_discountcode', 'OLP staff add discountcode'),
            ('staff_view_discountcode', 'OLP staff view discountcode'),
            ('staff_change_discountcode', 'OLP staff change discountcode'),
            ('staff_delete_discountcode', 'OLP staff delete discountcode'),
        ]

    def save(self, *args, **kwargs):

        self.code = self.code.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        if self.discount_percentage:
            return self.code + ', ' + str(self.discount) + '%' + '. Disponible desde:' + str(self.enabled_from) + ', hasta:' + str(self.enabled_to) + '.'
        elif self.discount_shipping and self.discount != 100:
            return self.code + ', ' + str(self.discount) + f'% en el envio' + '. Disponible desde:' + str(self.enabled_from) + ', hasta:' + str(self.enabled_to) + '.'
        else:
            return self.code + ', ' + 'envio gratis' + '. Disponible desde:' + str(self.enabled_from) + ', hasta:' + str(self.enabled_to) + '.'


class Order(models.Model):
    cash_type = [
        ('pagofacil', 'pagofacil'),
        ('rapipago', 'rapipago'),
        ('western union', 'western union')
    ]
    wallet_type = [
        ('paypal', 'paypal'),
        ('mercadopago', 'mercadopago'),
        ('brubank', 'brubank')
    ]
    status_choices = [
        ('incomplete', 'incomplete'),
        ('expired', 'expired'),
        ('approved', 'approved'),
        ('pending', 'pending'),
        ('denied', 'denied')
    ]

    token = models.CharField(max_length=64, blank=True, unique=True,)
    owner = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, verbose_name=_("Usuario"))

    items = models.ManyToManyField(
        Product, through="OrderItem", related_name="orders", verbose_name=_("Productos"))
    products_price = models.IntegerField(verbose_name=_(""))
    pay_method = models.CharField(
        max_length=100, null=True, verbose_name=_("Precio de Productos"))
    paymethod_cash_type = models.CharField(
        max_length=17, null=True, blank=True, choices=cash_type, verbose_name=_("Metodo pago en efectivo"))
    pay_method_card = models.ForeignKey(
        CardUser, on_delete=models.DO_NOTHING, null=True, blank=True, verbose_name=_("Tarjeta usada"))
    paymethod_wallet_type = models.CharField(
        max_length=15, null=True, blank=True, choices=wallet_type, verbose_name=_("Metodo Billetera virtual"))

    shipping_method = models.CharField(
        max_length=50, null=True, verbose_name=_("Metodo de envio"))
    shipping_price = models.IntegerField(
        null=True, blank=True, verbose_name=_("Precio de envio"))
    shipping_arrives = models.DateField(
        null=True, blank=True, verbose_name=_("Fecha de arribo"))
    address = models.ForeignKey(
        Address, on_delete=models.SET_NULL, null=True, verbose_name=_("Dirección"))

    total_to_pay = models.DecimalField(
        max_digits=10, decimal_places=2, default=000, verbose_name=_("Total a pagar"))
    discount_code = models.ForeignKey(
        DiscountCode, on_delete=models.SET_NULL, null=True, blank=True, verbose_name=_("Codigo de descuento"))
    discount_amount = models.IntegerField(
        null=True, verbose_name=_("Monto de descontado"))

    billing_status = models.BooleanField(
        default=False, verbose_name=_("Pagado?"))
    status = models.CharField(
        max_length=12, default='incomplete', choices=status_choices, verbose_name=_("Status"))

    created_at = models.DateTimeField(auto_now_add=True, null=True)
    expiration_date = models.DateTimeField(null=True)
    pay_received_date = models.DateTimeField(null=True)

    emition_cash_date = models.DateTimeField(
        null=True, verbose_name=_("Emision de pago en efectivo"))
    expiration_cash_date = models.DateTimeField(
        null=True, verbose_name=_("Expiración de pago en efectivo"))

    class Meta:
        verbose_name_plural = _("Ordenes")

    def save(self, *args, **kwargs):
        if not self.token:
            # Generate a token for the order ID using SHA-256 hashing
            salt = str(uuid.uuid4())

            self.token = hashlib.sha256(
                (salt + str(self.id)).encode('utf-8')).hexdigest()
        super(Order, self).save(*args, **kwargs)

    def __str__(self):
        return str(self.owner) + ", $" + str(self.total_to_pay) + ". " + str(self.billing_status)


class OrderItem(BaseItem):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

    class Meta:
        constraints = [models.UniqueConstraint(
            fields=['product', 'order'], name='unique_product_order')]

    def __str__(self):
        return self.product.name


class ProductBuyed(BaseItem):
    owner = models.ForeignKey(
        MyUser, on_delete=models.CASCADE, verbose_name=_("Comprado por"))
    buyed_at = models.DateTimeField(
        auto_now_add=True, verbose_name=_("Fecha de compra"))
    order = models.ForeignKey(
        Order, on_delete=models.SET_NULL, null=True, verbose_name=_("Orden"))

    class Meta:
        verbose_name_plural = _("Productos comprados")
        permissions = [
            ('staff_add_productbuyed', 'OLP staff add productbuyed'),
            ('staff_view_productbuyed', 'OLP staff view productbuyed'),
            ('staff_change_productbuyed', 'OLP staff change productbuyed'),
            ('staff_delete_productbuyed', 'OLP staff delete productbuyed'),
        ]

    def __str__(self):
        return self.owner.username + ', ' + self.product.name


@receiver(post_save, sender=DiscountCode)
def user_post_save(sender, instance, **kwargs):
    staff_group, created = Group.objects.get_or_create(name='Staff')

    assign_perm('staff_view_discountcode', staff_group, instance)

    assign_perm('staff_view_discountcode', instance.add_by, instance)
    assign_perm('staff_change_discountcode', instance.add_by, instance)
    assign_perm('staff_delete_discountcode', instance.add_by, instance)


@receiver(post_save, sender=ProductBuyed)
def user_post_save(sender, instance, **kwargs):
    staff_group, created = Group.objects.get_or_create(name='Staff')

    assign_perm('staff_view_productbuyed', staff_group, instance)

    assign_perm('staff_view_productbuyed', instance.owner, instance)
