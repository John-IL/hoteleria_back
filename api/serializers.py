from rest_framework import serializers
from .models import Product, ProductCategory, ProductFamliy


class ProductFamilySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductFamliy
        fields = ('id', 'name')


class ProductCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductCategory
        fields = ('id','name','family')

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ('id','name','stock','category')