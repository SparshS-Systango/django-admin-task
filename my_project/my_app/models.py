from __future__ import unicode_literals

from django.contrib.auth.models import User
from django.db import models


class Vendor(models.Model):
    brand_name = models.TextField(blank=True, default='', null=True, max_length=30)
    economic_model = models.CharField(max_length=40, null=False, blank=False, default="partnership")

    def __str__(self):
        return '{} - {}'.format(self.brand_name, self.id)


class Company(models.Model):
    users = models.ManyToManyField(User, related_name='users', through='CompanyUsers', through_fields=('company', 'user'))
    brand_name = models.TextField(blank=True, default='', null=True, max_length=30)
    reseller = models.ForeignKey(Vendor, on_delete=models.SET_NULL, related_name="companies", null=True)
    hidden_field = models.CharField(max_length=40)


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="profile", null=True, blank=True)
    vendor = models.ForeignKey(Vendor, on_delete=models.SET_NULL, related_name="user_profiles", null=True)
    first_name = models.CharField(max_length=200, null=True)
    hidden_fields = models.CharField(max_length=200, null=True)


class PricingPlan(models.Model):
    product_name = models.CharField(max_length=100, null=False, blank=False)
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="pricingplans", null=False)
    fee = models.IntegerField(null=False)
    scope = models.CharField(max_length=50, null=False, blank=False)
    status = models.CharField(max_length=20, null=False, default="open")  # open / closed


class VendorPricingPlan(models.Model):
    vendor = models.ForeignKey(Vendor, related_name='vendor_pricing_plans', on_delete=models.CASCADE)
    economic_model = models.CharField(max_length=20, default='retrocom')
    product_name = models.CharField(max_length=200, blank=True, default='')
    yavin_fee = models.IntegerField()
    suggested_fee = models.IntegerField()

    def __str__(self):
        return self.product_name


class CompanyUsers(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('company', 'user')
        verbose_name = 'Relation Company - User'
        verbose_name_plural = 'Relations Company - User'
