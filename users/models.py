from datetime import timedelta
from uuid import uuid4

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):
    """Define a model manager for User model with no username field."""

    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class CustomUserManager(UserManager):

    def get_queryset(self):
        return super().get_queryset().filter(deleted=False)


# todo: add validation for email.
class User(AbstractUser):
    id = models.UUIDField(default=uuid4, primary_key=True)
    email = models.CharField(max_length=150, unique=True, db_index=True)
    email_verified = models.CharField(max_length=150, null=True, blank=True)

    username = None

    objects = CustomUserManager()
    allobjects = UserManager()

    deleted = models.BooleanField(default=False)
    deleted_at = models.DateTimeField(null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        ordering = ['id']

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if not getattr(self, 'subscription', None):
            Subscription.objects.create(user=self)

    def delete(self, *args, **kwargs):
        self.deleted = True
        self.deleted_at = timezone.now()
        self.save(force_update=True)

    def __str__(self):
        return f"{self.id} | {self.email}"


class StripsCustomer(models.Model):
    user = models.OneToOneField(User,
                                on_delete=models.CASCADE,
                                related_name='strips_customer',
                                related_query_name='strips_customer'
                                )
    customer_id = models.CharField(max_length=50, null=True, blank=True)
    user_creation_timestamp = models.DateTimeField(null=True, blank=True)
    default_currency = models.CharField(max_length=4, null=True, blank=True)
    invoice_prefix = models.CharField(max_length=10, null=True, blank=True)
    phone = models.CharField(max_length=15, null=True, blank=True)


class Subscription(models.Model):
    class UserSubscriptionPlan(models.IntegerChoices):
        FREE = 0
        THREE_MONTHS = 3
        ONE_YEAR = 12

    id = models.CharField(max_length=50, primary_key=True, db_index=True)
    user = models.ForeignKey("User",
                             on_delete=models.CASCADE,
                             related_name='subscription',
                             related_query_name='subscription'
                             )
    creation_date = models.DateTimeField(auto_now_add=True)
    subscription_plan = models.IntegerField(choices=UserSubscriptionPlan.choices,
                                            default=UserSubscriptionPlan.FREE.value
                                            )
    current_period_start = models.DateTimeField
    current_period_end = models.DateTimeField()

    class Meta:
        ordering = ['id']

    @property
    def expiration_date(self):
        if self.subscription_plan != self.UserSubscriptionPlan.FREE.value:
            return self.creation_date + timedelta(days=self.subscription_plan * 30)
