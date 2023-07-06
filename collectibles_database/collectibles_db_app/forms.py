from django import forms
from . import models


class CreateItemForm(forms.ModelForm):
    class Meta:
        model = models.CollectibleItem
        fields = ('user', 'country', 'currency', 'release_year', 'circulation', 
                    'item_type', 'denomination', 'quantity', 'condition', 'description', 
                    'obverse_side', 'reverse_side', 'update_date')
        widgets = {
            'user' : forms.HiddenInput(),
            'update_date' : forms.HiddenInput(),
        }
        