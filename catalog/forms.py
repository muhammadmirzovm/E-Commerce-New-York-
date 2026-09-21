from django import forms
from .models import Product

class ProductForm(forms.ModelForm):
   class Meta:
       model = Product
       fields = (
           "category","name","price","short_description",
           "description","stock","is_active","main_image"
       )