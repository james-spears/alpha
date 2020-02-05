"""
    defines registrar related serializers
"""
from base64 import b64encode
from django.core.files import File
from rest_framework import serializers
from . import models


class UserCheckSerializer(serializers.HyperlinkedModelSerializer):
    """
        defines user serializer
    """
    class Meta:
        model = models.AlphaUser
        fields = ('username', 'id')


class ModuleSerializer(serializers.HyperlinkedModelSerializer):
    """
        defines user serializer
    """
    class Meta:
        model = models.Module
        fields = ('module_name', 'url', 'id')


class Oauth2EndpointSerializer(serializers.HyperlinkedModelSerializer):
    """
        defines user serializer
    """
    class Meta:
        model = models.Oauth2Endpoint
        fields = ('provider', 'url', 'id')


class ApiKeySerializer(serializers.HyperlinkedModelSerializer):
    """
        defines user serializer
    """
    class Meta:
        model = models.ApiKey
        fields = ('name', 'url', 'id')


class CompanySerializer(serializers.ModelSerializer):
    """
        defines user serializer
    """
    company_logo_b64 = serializers.SerializerMethodField()

    class Meta:
        model = models.Company
        fields = ('company_id', 'company_name', 'company_logo_b64', 'id')

    def get_company_logo_b64(self, obj):
        """
            This method will ensure images are returned
            in a base64 ecoded format.
        """
        company_logo_file = open(obj.company_logo.path, 'rb')
        image = File(company_logo_file)
        data = b64encode(image.read())
        company_logo_file.close()
        return data
