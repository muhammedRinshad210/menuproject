
from django import forms
from .models import Carousel, MenuItem


class CarouselForm(forms.ModelForm):
    class Meta:
        model = Carousel
        fields = "__all__"


class MenuItemForm(forms.ModelForm):
    class Meta:
        model = MenuItem
        fields = "__all__"


from django import forms
from .models import SpecialItem

class SpecialItemForm(forms.ModelForm):
    class Meta:
        model = SpecialItem
        fields = ['name', 'image', 'price', 'quantity', 'description']

        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter item name'
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'price': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter price'
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter stock quantity',
                'min': '0'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Enter description (optional)'
            }),
        }