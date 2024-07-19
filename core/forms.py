from django import forms
from core.models import Product
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget



class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter product name'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'desc': forms.Textarea(attrs={'class': 'form-control', 'rows': 1,  'placeholder': 'Enter product description'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.01', 'placeholder': 'Enter price'}),
            'product_available_count': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Enter available count'}),
            'img': forms.FileInput(attrs={'class': 'form-control-file'}),
        }


class CheckoutForm(forms.Form):
    street_address = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : '1234 BTM 2nd Stage'
    }))
    apartment_address = forms.CharField(required=False, widget=forms.TextInput(attrs={
        'class' : 'form-control',
        'placeholder' : 'apartment or building'
    }))
    country = CountryField(blank_label = '(--- select country ----').formfield(widget=CountrySelectWidget(attrs={
        'class': 'custom-select d-block w-100'
    }))
    zip_code = forms.CharField(widget=forms.TextInput(attrs={
        'class' : 'form-control'
    }))
