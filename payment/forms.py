from django import forms
from captcha.fields import ReCaptchaField
from captcha.widgets import ReCaptchaV2Invisible

from .models import Address, Card, DiscountCode, ProductBuyed


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        exclude = ["owner"]


class CardForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Invisible())


class CreateDisCode(forms.ModelForm):
    discount_kind = forms.CharField(widget=forms.RadioSelect(
        choices=DiscountCode.discount_kind_choices))

    class Meta:
        model = DiscountCode
        fields = ['code', 'discount_kind',
                  'discount', 'enabled_from', 'enabled_to']


class DiscountCodeAdminForm(forms.ModelForm):
    discount_kind = forms.CharField(widget=forms.RadioSelect(
        choices=DiscountCode.discount_kind_choices))

    class Meta:
        model = DiscountCode
        fields = ['add_by', 'code', 'discount_kind',
                  'discount', 'enabled_from', 'enabled_to']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if not self.instance.pk:
            self.fields['add_by'].widget.attrs['readonly'] = True
            self.fields['add_by'].disabled = True
