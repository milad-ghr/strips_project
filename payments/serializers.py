from rest_framework import serializers

from users.serializers import SubscriptionSerializer
from api_connections.strips_connections import StripConnection
from products.serializers import ProductSerializer, Product
from .models import Payment, Card


class CardSerializer(serializers.ModelSerializer):
    class Meta:
        model = Card
        fields = ['id', 'number', 'expiration_year', 'expiration_month', 'cvc']

    def validate(self, attrs):
        if len(attrs['number']) != 16:
            raise serializers.ValidationError("Card Number must be 16 digits")
        return attrs

    def to_representation(self, instance: Card):
        representation = super().to_representation(instance)
        representation['number'] = representation['number'][0:4] + 8 * '*' + representation['number'][12:16]
        return representation


class PaymentSerializer(serializers.ModelSerializer):
    card = CardSerializer(read_only=True)
    card_id = serializers.PrimaryKeyRelatedField(queryset=Card.objects.all(), write_only=True)
    subscription = SubscriptionSerializer(read_only=True)
    product = ProductSerializer(read_only=True)
    product_id = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all(), write_only=True)

    class Meta:
        model = Payment
        fields = ['id', 'card', 'payment_method', 'payment_id', 'subscription',
                  'product', 'creation_date', 'modification_date']

    def create(self, validated_data):
        card_obj = validated_data['card_id']
        product_obj = validated_data['product_id']
        user = self.context['request'].user
        strips_api_object = StripConnection(user=user,
                                            product_object=product_obj,
                                            )
        payment_method_object = strips_api_object.handle(card_obj=card_obj)
        return payment_method_object

