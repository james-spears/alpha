"""
    This module contains the registrar
    models.
"""
import os
from urllib import parse
from base64 import b64encode
from time import strftime
from uuid import uuid4
from django.contrib.auth.models import AbstractUser
from django.db import models
# Create your models here.

class AlphaUser(AbstractUser):
    """
        This class defines the alpha user.
    """

class BaseEndpoint(models.Model):
    """
        This class defines the endpoint model
        used which is a base class.
    """
    url = models.URLField(
        max_length=512,
        blank=False,
        null=False,
        unique=True
    )

    class Meta:
        abstract = True

    def __str__(self):
        return self.url

class Module(BaseEndpoint):
    """
        This class defines the module
        model.
    """
    module_name = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        unique=True
    )

    def url_safe_module_name(self):
        """
            A convenience method which returns
            the url encoded company name
            property
        """
        return parse.quote(self.module_name)

    def __str__(self):
        return self.module_name

class Oauth2Endpoint(BaseEndpoint):
    """
        This class defines the Oauth2 mode
        for a Social Auth Provider.
    """
    provider = models.CharField(
        max_length=64,
        blank=False,
        null=False,
        unique=True
    )

    def __str__(self):
        return self.provider


class ApiKey(BaseEndpoint):
    """
        This class defines a generic api
        key.
    """
    api_key = models.CharField(
        max_length=2048,
        blank=False,
        null=False,
        unique=True
    )
    name = models.CharField(
        max_length=64,
        blank=False,
        null=False,
        unique=True
    )

    def __str__(self):
        return self.name

    def b64encoded_api_key(self):
        """
            A convenience method which returns
            the base 64 encoded api key
            property.
        """
        return b64encode(self.api_key)

def get_file_path(_, filename):
    """
        Helper to change file name to uuid
        when image instanse is instantiated.
    """
    ext = filename.split('.')[-1]
    filename = "%s.%s" % (uuid4(), ext)
    return os.path.join(
        strftime('uploads/%Y/%m/%d'),
        filename
    )

class Company(models.Model):
    """
        This class defines the company
        model.
    """
    company_id = models.CharField(
        max_length=64,
        blank=False,
        null=False,
        unique=True
    )
    company_name = models.CharField(
        max_length=256,
        blank=False,
        null=False,
        unique=True
    )
    company_logo = models.ImageField(
        upload_to=get_file_path
    )

    class Meta:
        verbose_name_plural = "companies"

    def url_safe_company_name(self):
        """
            A convenience method which returns
            the url encoded company name
            property
        """
        return parse.quote(self.company_name)

    def __str__(self):
        return self.company_name
