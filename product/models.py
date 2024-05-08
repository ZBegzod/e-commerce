from django.contrib.auth.models import User
from django.db import models


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return f"{self.name}"


class Product(BaseModel):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name='products'
    )
    name = models.CharField(max_length=150)
    price = models.IntegerField(default=0)
    count = models.IntegerField(default=0)
    image = models.ImageField(
        upload_to='images/products/',
        blank=True, null=True
    )
    description = models.TextField(
        max_length=1000, null=True, blank=True)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        ordering = ['-created_at']


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images')
    image = models.ImageField(upload_to='images/products/')


class Order(BaseModel):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    total = models.FloatField(blank=True, null=True)
    comment = models.CharField(null=True, blank=True, max_length=255)

    class Meta:
        ordering = ['-created_at']


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order, on_delete=models.CASCADE,
        related_name='order_items')

    product = models.ForeignKey(
        Product, on_delete=models.SET_NULL,
        related_name='order_product_items',
        blank=True, null=True)

    quantity = models.IntegerField(default=1)
