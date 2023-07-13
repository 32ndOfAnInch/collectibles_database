from django import forms
from . import models

class CreateItemForm(forms.ModelForm):
    condition = forms.ModelChoiceField(
        queryset=models.GradationSystem.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_condition'})
    )
    value = forms.ModelChoiceField(
        queryset=models.Value.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_value'})
    )

    class Meta:
        model = models.CollectibleItem
        fields = (
            'user', 'country', 'currency', 'release_year', 'circulation',
            'item_type', 'denomination', 'quantity', 'condition', 'value',
            'description', 'obverse_side', 'reverse_side', 'update_date'
        )
        widgets = {
            'user': forms.HiddenInput(),
            'update_date': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['value'].queryset = models.Value.objects.none()

        if 'condition' in self.data:
            try:
                condition_id = int(self.data.get('condition'))
                self.fields['value'].queryset = models.Value.objects.filter(
                    gradation_system_id=condition_id)
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['value'].queryset = self.instance.condition.value.all()

class UpdateItemForm(forms.ModelForm):
    condition = forms.ModelChoiceField(
        queryset=models.GradationSystem.objects.all(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_condition'})
    )
    value = forms.ModelChoiceField(
        queryset=models.Value.objects.none(),
        widget=forms.Select(attrs={'class': 'form-control', 'id': 'id_value'})
    )

    class Meta:
        model = models.CollectibleItem
        fields = (
            'user', 'country', 'currency', 'release_year', 'circulation',
            'item_type', 'denomination', 'quantity', 'condition', 'value',
            'description', 'obverse_side', 'reverse_side', 'update_date'
        )
        widgets = {
            'user': forms.HiddenInput(),
            'update_date': forms.HiddenInput(),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['value'].queryset = models.Value.objects.none()

        if 'condition' in self.data:
            try:
                condition_id = int(self.data.get('condition'))
                self.fields['value'].queryset = models.Value.objects.filter(
                    gradation_system_id=condition_id
                )
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['value'].queryset = self.instance.condition.values.all()
            