from rest_framework import serializers

from .models import Product


class ProductSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = ['id', 'creation_date', 'name', 'active', 'description', 'price_unit', 'price', 'duration_unit',
                  'duration', 'product_id', 'related_image']
