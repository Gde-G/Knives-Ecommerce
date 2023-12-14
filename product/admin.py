from typing import Any
from django.contrib import admin
from django.shortcuts import redirect
from django.http.request import HttpRequest
from .models import *
from guardian.admin import GuardedModelAdmin
from guardian.shortcuts import get_objects_for_user
from django.db import IntegrityError
from django.contrib import messages

from .forms import CategoryAdminForm, HandleAdminForm, ProductAdminForm, Prod_SecImgAdminForm, Prod_SecImgFormSet, MessageAdminForm


class BaseAdminOLP(GuardedModelAdmin, admin.ModelAdmin):
    def has_module_permission(self, request: HttpRequest):
        if request.user.is_superuser:
            return True
        return self.get_model_objects(request).exists()

    def get_queryset(self, request: HttpRequest):
        if request.user.is_superuser:
            return super().get_queryset(request)
        data = self.get_model_objects(request)
        return data

    def get_model_objects(self, request: HttpRequest, action=None, klass=None):
        opts = self.opts
        actions = [action] if action else ['view', 'edit', 'delete']
        klass = klass if klass else opts.model
        model_name = klass._meta.model_name
        return get_objects_for_user(user=request.user, perms=[f'{perm}_{model_name}' for perm in actions]+[f'staff_{perm}_{model_name}' for perm in actions], klass=klass, any_perm=True)

    def has_permission(self, request: HttpRequest, obj, action):
        opts = self.opts
        code_name = f'{action}_{opts.model_name}'
        if obj:

            return request.user.has_perm(f'{opts.app_label}.{code_name}', obj) or request.user.has_perm(f'{opts.app_label}.staff_{code_name}', obj)
        else:
            return self.get_model_objects(request).exists()

    def has_view_permission(self, request: HttpRequest, obj=None):
        if request.user.is_superuser:
            return True
        return self.has_permission(request, obj, 'view')

    def has_change_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return self.has_permission(request, obj, 'change')

    def has_delete_permission(self, request, obj=None):
        if request.user.is_superuser:
            return True
        return self.has_permission(request, obj, 'delete')


class CategoryAdmin(BaseAdminOLP):
    def get_form(self, request, obj=None, **kwargs):
        form = CategoryAdminForm

        try:
            form.base_fields['add_by'].initial = request.user.id
        except:
            pass
        return form

    list_display = ('name', 'add_by')


class HandleAdmin(BaseAdminOLP):
    def get_form(self, request, obj=None, **kwargs):
        form = HandleAdminForm
        try:
            form.base_fields['add_by'].initial = request.user.id
        except:
            pass
        return form

    list_display = ('material', 'add_by')


class Prod_SecImgInline(admin.StackedInline):
    model = Prod_SecImg
    form = Prod_SecImgAdminForm
    formset = Prod_SecImgFormSet
    extra = 1
    max_num = 1


class ProductAdmin(admin.ModelAdmin):
    form = ProductAdminForm
    inlines = [Prod_SecImgInline]
    list_display = ("name", "price", "add_by", "stock")

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)

        try:
            form.base_fields['add_by'].initial = request.user.id
        except:
            pass
        return form

    def save_related(self, request, form, formsets, change):
        super().save_related(request, form, formsets, change)

        product = form.instance
        img_primary = form.cleaned_data.get('img_primary')

        for formset in formsets:
            if isinstance(formset, Prod_SecImgFormSet):
                prod_sec_img_formset = formset
                break
        else:
            return

        try:
            prod_sec_img = Prod_SecImg.objects.get(prod=product)
            prod_sec_img.img_sec_1 = img_primary
            prod_sec_img.save()
        except Prod_SecImg.DoesNotExist:
            Prod_SecImg.objects.create(prod=product, img_sec_1=img_primary)


class Prod_SecImgAdmin(BaseAdminOLP):
    list_display = ("prod", "img_sec_1", "img_sec_2",
                    "img_sec_3", "img_sec_4", "img_sec_5")


class MessageAdmin(BaseAdminOLP):
    list_display = ("user", "product", "have_answered")

    def get_form(self, request, obj=None, **kwargs):
        form = MessageAdminForm

        try:
            form.base_fields['add_by'].initial = request.user.id
        except:
            pass

        return form


admin.site.register(Category, CategoryAdmin)
admin.site.register(Handle, HandleAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Prod_SecImg, Prod_SecImgAdmin)
admin.site.register(Message, MessageAdmin)
