# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import status, viewsets
from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.utils import timezone
from graphene_django import DjangoObjectType
import graphene

# Create your models here.
class CarPurchases(models.Model):
    vin = models.CharField(max_length=20, null=False)
    vehicle_make = models.CharField(max_length=20, default="n/a")
    year = models.IntegerField()
    model_name = models.CharField(max_length=20, default="n/a")
    mileage = models.IntegerField()
    unit_of_measurement = models.CharField(max_length=20, default="n/a")
    exterior_color = models.CharField(max_length=10, default="n/a")
    seller_name = models.CharField(max_length=20, default="n/a")
    purchase_date = models.DateTimeField(null=True)
    total_hst = models.CharField(max_length=20, default="n/a")
    total_price = models.CharField(max_length=20, default="n/a")

class CarFax(models.Model):
    vin = models.CharField(max_length=20)
    structural_damage = models.CharField(max_length=100, default="Check Online")
    total_loss = models.CharField(max_length=100, default="Check Online")
    accident = models.CharField(max_length=100, default="Check Online")
    airbags = models.CharField(max_length=100, default="Check Online")
    odometer = models.CharField(max_length=100, default="Check Online")

class ShoppingList(models.Model):
    vin = models.CharField(max_length=20, null=False)
    vehicle_make = models.CharField(max_length=20, default="n/a")
    year = models.IntegerField()
    model_name = models.CharField(max_length=20, default="n/a")
    mileage = models.IntegerField()
    unit_of_measurement = models.CharField(max_length=20, default="n/a")
    exterior_color = models.CharField(max_length=10, default="n/a")
    seller_name = models.CharField(max_length=20, default="n/a")
    purchase_date = models.DateTimeField(null=True)
    total_hst = models.CharField(max_length=20, default="n/a")
    total_price = models.CharField(max_length=20, default="n/a")