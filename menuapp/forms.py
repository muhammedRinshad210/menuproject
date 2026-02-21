
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
        fields = '__all__'
