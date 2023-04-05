from django.db import models
from django.core.validators import MinValueValidator

# Create your models here.

class ProductFamliy(models.Model):
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

class ProductCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)
    family = models.ForeignKey(ProductFamliy, on_delete=models.CASCADE, verbose_name='product family relation')
    created_at = models.DateTimeField(auto_now_add=True)


class Product(models.Model):
    name = models.CharField(max_length=50, unique=True)
    stock = models.IntegerField(validators=[MinValueValidator(0)])
    category = models.ForeignKey(ProductCategory, on_delete=models.CASCADE, verbose_name='product category relation' )
    status = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)