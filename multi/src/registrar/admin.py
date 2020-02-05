"""
    Here all of the models are
    registered with the admin
    console.
"""
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

# Register your models here.
from . import models
from . import forms

class ApiKeyAdmin(admin.ModelAdmin):
    """
        Here we override the default admin
        form to hide the api key like a
        password.
    """
    form = forms.ApiKeyForm

admin.site.register(models.ApiKey, ApiKeyAdmin)
admin.site.register(models.AlphaUser, UserAdmin)
admin.site.register(models.Oauth2Endpoint)
admin.site.register(models.Company)
admin.site.register(models.Module)
