"""
    Here is where the we define the custom
    form classes.
"""
from django.forms import ModelForm, PasswordInput, TextInput
from . import models

class ApiKeyForm(ModelForm):
    """
        We want to define a custom
        api key form that hides the
        api key like a password.
    """
    class Meta:
        model = models.ApiKey
        fields = '__all__'
        widgets = {
            "api_key": PasswordInput(),
            "name": TextInput()
        }
