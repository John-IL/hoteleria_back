from rest_framework import serializers
from api import models


class RoleSerializer (serializers.ModelSerializer):
    class Meta:
        model = models.Roles
        fields = ('id', 'name')

class DocumentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StaticDocumentTypes
        fields = ('id', 'name')


class CountrySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.StaticCountries
        fields = ('id', 'name', 'iso')