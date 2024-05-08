from django import forms
from .models import *


class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['id', 'name']


class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ['id', 'name', 'price', 'count', 'description']


class OrderItemForm(forms.ModelForm):
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['id', 'user', 'total', 'comment']

