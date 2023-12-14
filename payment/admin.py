from django.contrib import admin
from django.shortcuts import redirect
from product.admin import BaseAdminOLP

from .models import *
from .forms import DiscountCodeAdminForm


class DiscountCodeAdmin(BaseAdminOLP):
    list_display = ("code", "discount", "discount_kind", "add_by")

    def get_form(self, request, obj=None, **kwargs):
        form = DiscountCodeAdminForm

        try:
            form.base_fields['add_by'].initial = request.user.id
        except:
            pass

        return form


class ProductBuyedAdmin(BaseAdminOLP):
    list_display = ("product", "owner", "buyed_at")


admin.site.register(Address)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Card)
admin.site.register(CardUser)
admin.site.register(DiscountCode, DiscountCodeAdmin)
admin.site.register(ProductBuyed, ProductBuyedAdmin)
