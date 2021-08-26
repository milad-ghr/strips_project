from django.db import models
from django_cryptography.fields import encrypt

from products.models import Product
from users.models import Subscription, StripsCustomer


class PaymentsManager(models.Manager):
    pass


class PaymentsManagerWithNoDeleted(models.Manager):

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


class AbstractPaymentModel(models.Model):
    creation_date = models.DateTimeField(auto_now_add=True)
    modification_date = models.DateTimeField(auto_now=True)

    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    objects = PaymentsManagerWithNoDeleted()
    allobjects = PaymentsManager()

    class Meta:
        abstract = True


class Card(models.Model):
    number = encrypt(models.CharField(max_length=16, unique=True))
    expiration_month = encrypt(models.CharField(max_length=2))
    expiration_year = encrypt(models.CharField(max_length=4))
    cvc = encrypt(models.CharField(max_length=4))
    brand = models.CharField(max_length=15, null=True, blank=True)
    country = models.CharField(max_length=10, null=True, blank=True)
    fingerprint = encrypt(models.CharField(max_length=30, null=True, blank=True))
    funding = models.CharField(max_length=10, null=True, blank=True)

    class Meta:
        ordering = ['id']


class Payment(AbstractPaymentModel):
    class PaymentMethodsChoices(models.IntegerChoices):
        CARD = 1

    payment_method = models.IntegerField(choices=PaymentMethodsChoices.choices,
                                         default=PaymentMethodsChoices.CARD.value
                                         )
    payment_id = models.CharField(max_length=50, null=True, blank=True)
    strip_customer = models.ForeignKey(StripsCustomer,
                                       on_delete=models.SET_NULL,
                                       null=True,
                                       related_name='payments',
                                       related_query_name='payment'
                                       )
    card = models.ForeignKey(Card,
                             on_delete=models.SET_NULL,
                             null=True,
                             related_name='payments',
                             related_query_name='payment'
                             )
    subscription = models.OneToOneField(Subscription,
                                        on_delete=models.SET_NULL,
                                        null=True,
                                        related_name='payment',
                                        related_query_name='payment'
                                        )
    product = models.ForeignKey(Product,
                                on_delete=models.SET_NULL,
                                null=True,
                                related_name='payments',
                                related_query_name='payment'
                                )
    billing_detail = models.JSONField(null=True, blank=True)

    class Meta:
        ordering = ['id']
