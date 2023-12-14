from typing import Any, Dict
from django import forms
from django.forms.models import inlineformset_factory
from django.contrib import messages

from .models import Category, Handle, Product, Prod_SecImg, Message


class SearchForm(forms.Form):
    query = forms.CharField(max_length=100)


class CreateCategory(forms.ModelForm):

    class Meta:
        model = Category
        fields = ['name', 'description']


class CreateHandle(forms.ModelForm):

    class Meta:
        model = Handle
        fields = ['material']


class CreateProduct(forms.ModelForm):

    class Meta:
        model = Product
        fields = ['name', 'description', 'img_primary', 'category',
                  'handle', 'price', 'blade_material', 'blade_size', 'handle_size']


class CreateProd_SecImg(forms.ModelForm):

    class Meta:
        model = Prod_SecImg
        fields = ['img_sec_2', 'img_sec_3', 'img_sec_4', 'img_sec_5']


class CreateMessage(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['body']


class CreateMessageAwnser(forms.ModelForm):

    class Meta:
        model = Message
        fields = ['answer']


class CategoryAdminForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['add_by', 'name', 'description']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['add_by'].widget.attrs['readonly'] = True
            self.fields['add_by'].disabled = True

    def save(self, commit: bool = ...) -> Any:
        if self.is_valid():
            return super().save(commit)
        else:
            print('HEREEE')


class HandleAdminForm(forms.ModelForm):
    class Meta:
        model = Handle
        fields = ['add_by', 'material']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['add_by'].widget.attrs['readonly'] = True
            self.fields['add_by'].disabled = True


class Prod_SecImgAdminForm(forms.ModelForm):
    class Meta:
        model = Prod_SecImg
        fields = ['img_sec_2', 'img_sec_3', 'img_sec_4', 'img_sec_5']


class ProductAdminForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['add_by', 'name', 'description', 'img_primary', 'category',
                  'handle', 'price', 'quantity', 'stock', 'blade_material', 'blade_size', 'handle_size']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['add_by'].widget.attrs['readonly'] = True
            self.fields['add_by'].disabled = True


class BaseProductAdminFormSet(forms.BaseInlineFormSet):
    def clean(self):
        super().clean()

        has_product_form = any(
            self.cleaned_data and not form.errors for form in self.forms)

        has_prod_sec_img_form = any(
            self.cleaned_data and not form.errors for form in self.get_prod_sec_img_forms())

        if not has_product_form or not has_prod_sec_img_form:
            raise forms.ValidationError(
                "Please provide both Product and Prod_SecImg information.")

    def get_prod_sec_img_forms(self):
        for form in self.forms:
            if hasattr(form, 'cleaned_data') and any(form.cleaned_data.get(f) for f in ['img_sec_1', 'img_sec_2', 'img_sec_3', 'img_sec_4', 'img_sec_5']):
                yield form


Prod_SecImgFormSet = forms.inlineformset_factory(
    Product,
    Prod_SecImg,
    form=Prod_SecImgAdminForm,
    formset=BaseProductAdminFormSet,
    extra=1,
    max_num=1
)


class MessageAdminForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['user', 'product', 'body',
                  'have_answered', 'staff_user', 'answer']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['user'].widget.attrs['readonly'] = True
            self.fields['user'].disabled = True
