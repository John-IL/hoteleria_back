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

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.RoomCategory
        fields = ('id', 'name')

class FloorSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Floor
        fields = ('id', 'number')

class PromotionSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Promotion
        fields = ('id', 'name')