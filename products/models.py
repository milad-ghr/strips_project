from django.db import models


class Product(models.Model):

    creation_date = models.DateTimeField(auto_now_add=True)
    name = models.CharField(max_length=250, db_index=True, unique=True)
    active = models.BooleanField(default=True)
    description = models.TextField(null=True, blank=True)
    price_unit = models.CharField(max_length=3)
    price = models.FloatField(default=0)
    duration_unit = models.CharField(max_length=10, null=True, blank=True)
    duration = models.IntegerField(null=True, blank=True)
    product_id = models.CharField(max_length=50, null=True, blank=True)
    price_id = models.CharField(max_length=50, null=True, blank=True)
    related_image = models.FileField(null=True, blank=True, upload_to='products')

    class Meta:
        ordering = ['id']
