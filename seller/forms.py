from string import Template

from django import forms
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from core.models import *


class ProductCreateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductCreateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Product title'
        self.fields['price'].widget.attrs['placeholder'] = 'Product price'
        self.fields['stock_no'].widget.attrs['placeholder'] = 'SKU'
        self.fields['category'].empty_label = 'Choose category'
        self.fields['description_short'].widget.attrs['placeholder'] = 'Short description'
        self.fields['description_long'].widget.attrs['placeholder'] = 'Describe about your product'
        self.fields['discount_price'].widget.attrs['placeholder'] = 'Discount price(optional)'
        # label is char field that's why it doesn't contain empty_label
        self.fields["label"].choices = [("", "Choose label"), ] + list(self.fields["label"].choices)[1:]

    class Meta:
        model = Product
        exclude = ('user', 'slug')
        labels = {
            'discount_price': 'Discount price(optional)'
        }

    def save(self, commit=True):
        product = super(ProductCreateForm, self).save(commit=False)
        product.slug = slugify(product.title)
        if commit:
            product.save()
        return product


class ProductUpdateForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(ProductUpdateForm, self).__init__(*args, **kwargs)
        self.fields['title'].widget.attrs['placeholder'] = 'Product title'
        self.fields['price'].widget.attrs['placeholder'] = 'Product price'
        self.fields['stock_no'].widget.attrs['placeholder'] = 'SKU'
        self.fields['category'].empty_label = 'Choose category'
        self.fields['description_short'].widget.attrs['placeholder'] = 'Short description'
        self.fields['description_long'].widget.attrs['placeholder'] = 'Describe about your product'
        self.fields['discount_price'].widget.attrs['placeholder'] = 'Discount price(optional)'
        # label is char field that's why it doesn't contain empty_label
        self.fields["label"].choices = [("", "Choose label"), ] + list(self.fields["label"].choices)[1:]

    class Meta:
        model = Product
        exclude = ('user', 'slug')
        labels = {
            'discount_price': 'Discount price(optional)'
        }


class PictureWidget(forms.widgets.Widget):
    def render(self, name, value, attrs=None, **kwargs):
        html = Template("""<img src="$link"/>""")
        return mark_safe(html.substitute(link=value))


class SellerProfileUpdateForm(forms.ModelForm):
    preview_image = forms.ImageField(widget=PictureWidget)

    def __init__(self, *args, **kwargs):
        super(SellerProfileUpdateForm, self).__init__(*args, **kwargs)

    class Meta:
        model = Profile
        fields = ("shop_name", "image", "preview_image")
