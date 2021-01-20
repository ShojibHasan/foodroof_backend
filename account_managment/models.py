import uuid
from random import randint

from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser, User, UserManager
from django.db import models
from django.db.models import JSONField
from django.shortcuts import render
from django.utils import timezone
from django.utils.timezone import timedelta
from foodroof_backend.settings import TIME_ZONE
from softdelete.models import SoftDeleteModel

# Create your models here.


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        """
        Create and save a user with the given username, email, and password.
        """
        # if not username:
        #     raise ValueError('The given username must be set')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(
            # username=username, email=email,
            **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username=None, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(username, email, password, **extra_fields)


class UserAccount(AbstractUser):
    USERS_IN_STATUS_CHOICES = [
        ("ACT", "Active"),
        ("UNV", "Unverified"),
        ("BLK", "Blacked"),
        ("DEL", "Deleted"),
    ]
    username = None
    email = None
    #first_name = None
    last_name = None

    # email = models.EmailField(max_length=35, null=True, blank=True)
    phone = models.CharField(max_length=35, unique=True)
    status = models.CharField(max_length=25,
                              choices=USERS_IN_STATUS_CHOICES, default='UNV')

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = []
    objects = UserManager()

class CustomerInfo(models.Model):
    name = models.CharField(null=True, blank=True, max_length=250)
    email = models.EmailField(max_length=35, null=True, blank=True)
    date_of_birth = models.DateField(null=True, blank=True)
    user = models.OneToOneField(
        to=UserAccount, on_delete=models.CASCADE, related_name='customer_info')


class FoofRoofSellerInformation(SoftDeleteModel):
    # user = models.ForeignKey()
    DAYS_OF_WEEK = (
        ('Monday', 'Monday'),
        ('Tuesday', 'Tuesday'),
        ('Wednesday', 'Wednesday'),
        ('Thursday', 'Thursday'),
        ('Friday', 'Friday'),
        ('Saturday', 'Saturday'),
        ('Sunday', 'Sunday'),
    )
    user = models.ForeignKey(
        to=UserAccount,  on_delete=models.CASCADE, related_name='food_roof_seller')
    image = models.ImageField(null=True, blank=True)
    is_business = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)
    is_seller = models.BooleanField(default=False)
    nid = models.CharField(max_length=50, null=True, blank=True)
    name = models.CharField(null=True, blank=True, max_length=250)
    email = models.EmailField(null=True, blank=True)
    address = models.TextField(max_length=250,null=True,blank=True)
    phone = models.IntegerField()

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user'], name='seller')
        ]
