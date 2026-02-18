from django.db import models

class ProductType(models.Model):
    name = models.CharField(max_length=20, unique=True)

class Product(models.Model):
    CATEGORY_CHOICES = (
        ('MEN', 'MEN'),
        ('WOMEN', 'WOMEN'),
        ('KIDS', 'KIDS')
    )

    name = models.CharField(max_length=150)
    category = models.CharField(max_length=5, choices=CATEGORY_CHOICES)
    product_type = models.ForeignKey(ProductType, on_delete=models.CASCADE, related_name='items')
    description = models.TextField()
    price = models.DecimalField(max_digits=8, decimal_places=2)
    count = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name