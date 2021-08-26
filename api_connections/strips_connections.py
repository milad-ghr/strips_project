import requests
from urllib.parse import urljoin

from django.conf import settings

from users.models import Subscription, StripsCustomer
from payments.models import Payment, Card
from .abstract_connections import AbstractConnection


class StripConnection(AbstractConnection):
    DEFAULT_API_ENDPOINT = settings.STRIPS_API_ENDPOINT

    def __init__(self, *args, product_object=None, **kwargs):
        super().__init__(*args, **kwargs)
        if product_object:
            self.product_object = product_object
        else:
            self.product_object = None

    @staticmethod
    def _handle_headers():
        secret_key = settings.STRIPS_API_SECRET
        return {"Authorization": "Bearer " + secret_key}

    def _generate_url(self, endpoint: str):
        return urljoin(self.DEFAULT_API_ENDPOINT, endpoint)

    # todo: handle connection error
    def _request_api(self, method: str, endpoint: str, data: dict = None):
        headers_dict = self._handle_headers()
        url = self._generate_url(endpoint=endpoint)
        if method == 'get':
            response = requests.get(url, headers=headers_dict)
        elif method == 'post':
            response = requests.post(url, data=data, headers=headers_dict)
        else:
            raise ValueError("Only `post` and `get` methods have been defined.")
        if response.status_code == 200:
            return response.json()
        raise Exception(response.json())

    def create_payment_method(self, card_obj: Card):
        endpoint = "/v1/payment_methods"
        data = {
            "type": "card",
            "card[number]": card_obj.number,
            "card[exp_month]": int(card_obj.expiration_month),
            "card[exp_year]": int(card_obj.expiration_year),
            'card[cvc]': int(card_obj.cvc)
        }
        response = self._request_api(method='post', endpoint=endpoint, data=data)
        card_obj.brand = response['card']['brand']
        card_obj.country = response['card']['country']
        card_obj.fingerprint = response['card']['fingerprint']
        card_obj.funding = response['card']['funding']
        card_obj.save()

        payment_method_object = Payment.objects.create(payment_method=Payment.PaymentMethodsChoices.CARD.value,
                                                       payment_id=response['id'],
                                                       card=card_obj,
                                                       billing_detail=response['billing_details']
                                                       )

        return payment_method_object

    def update_payment_method(self, payment_object: Payment, update_data: dict = None):
        endpoint = f"/v1/payment_methods/{payment_object.payment_id}"
        data = {
            "customer": payment_object.strip_customer.customer_id,
            **update_data
        }
        response = self._request_api(method='post', endpoint=endpoint, data=data)
        return response

    def create_customer(self, payment_obj):
        if not self.user:
            raise ValueError("`user` must be set first.")
        endpoint = "/v1/customers"
        data = {
            "name": self.user.email,
            "payment_method": payment_obj.payment_id,
            "invoice_settings[default_payment_method]": payment_obj.payment_id
        }
        response = self._request_api(method='post', endpoint=endpoint, data=data)
        strip_customer_obj = StripsCustomer.objects.create(user=self.user,
                                                           customer_id=response['id'],
                                                           user_creation_timestamp=response['created'],
                                                           default_currency=response['currency'],
                                                           invoice_prefix=response['invoice_prefix'],
                                                           phone=response['phone'])
        payment_obj.strip_customer = strip_customer_obj
        payment_obj.save()
        return strip_customer_obj

    def create_subscription(self):
        if not self.user or not self.product_object:
            raise ValueError("`user` and `product_object` must be set.")
        endpoint = "/v1/subscriptions"
        data = {
            "customer": self.user.strips_customer.customer_id,
            "items[0][price]": self.product_object.price_id
        }
        response = self._request_api(method='post', endpoint=endpoint, data=data)
        subscription_object = Subscription.objects.create(id=response['id'],
                                                          user=self.user,
                                                          current_period_end=response['current_period_end'],
                                                          current_period_start=response['current_period_start'],
                                                          )
        return subscription_object

    def get_prices_with_product_id(self, product_id):
        endpoint = "/v1/prices"
        response = self._request_api(method='get', endpoint=endpoint)
        price_items = response['data']
        for item in price_items:
            if item['product'] == product_id:
                return item
        return None

    def get_products(self, product_id: str = None):
        if product_id:
            endpoint = f"/v1/products/{product_id}"
        else:
            endpoint = "/v1/products"
        product_dict = self._request_api('get', endpoint=endpoint)
        products_list = product_dict['data']
        return products_list

    def handle(self, card_obj: Card):
        if not self.product_object:
            raise ValueError("`product_object` must be set.")
        payment_method_object = self.create_payment_method(card_obj=card_obj)
        strip_customer = self.create_customer(payment_method_object)
        self.update_payment_method(payment_object=payment_method_object)
        subscription_obj = self.create_subscription()
        # Handle Webhook
        return payment_method_object
