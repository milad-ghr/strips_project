from rest_framework import serializers

from .models import Subscription, User, StripsCustomer


class StripsCustomerSerializer(serializers.ModelSerializer):

    class Meta:
        model = StripsCustomer
        fields = ['id', 'user', 'customer_id', 'user_creation_timestamp', 'default_currency', 'invoice_prefix',
                  'phone']


class UserSerializer(serializers.ModelSerializer):
    strips_customer = StripsCustomerSerializer(read_only=True)

    def __init__(self, *args, show_subscription=False, **kwargs):
        super().__init__(*args, **kwargs)
        if show_subscription:
            self.fields['subscription'] = SubscriptionSerializer(many=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'email', 'email_verified', 'phone', 'phone_verified',
                  'strips_customer']


class SubscriptionSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Subscription
        fields = ['id', 'user', 'creation_date', 'subscription_plan']

