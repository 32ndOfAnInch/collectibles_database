from django import forms
from django.contrib.auth import get_user_model

from . import models

User = get_user_model()


class UserUpdateForm(forms.ModelForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("first_name", "last_name", "username", "email")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ("picture",)

class UserPreferencesForm(forms.ModelForm):
    class Meta:
        model = models.Profile
        fields = ['paginate_by', 'color_theme', 'display_style', 'is_verification', 'is_notification']
        labels = {
            'paginate_by': 'Items per Page',
            'color_theme': 'Color Theme',
            'display_style': 'Display Style',
            'is_verification': 'Notifications',
            'is_notification': 'New Item Verification',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Modify the choices to display only the numbers
        self.fields['paginate_by'].choices = [
            (12, '12'),
            (24, '24'),
            (36, '36'),
            (48, '48'),
        ]
