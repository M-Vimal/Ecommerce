from django import forms
from ecommerce.models import Product,Category

class AddproductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = '__all__'
        exclude = ['seller']

        widgets = {
            'p_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Product Name'}),
            'price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Price'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'is_sale': forms.CheckboxInput(attrs={'class': 'form-check-input','id':'is_sale'}),
            'sale_price': forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Sale Price'}),
        }