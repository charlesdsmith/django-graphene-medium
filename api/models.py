# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from rest_framework import status, viewsets
from django.db import models
from django.contrib.postgres.fields import JSONField, ArrayField
from django.utils import timezone
from graphene_django import DjangoObjectType
import graphene

import time

# Create your models here.
class GetAdesaPurchases(models.Model):

    vin = models.CharField(max_length=20, null=False)
    vehicle_id = models.IntegerField()
    vehicle_make = models.CharField(max_length=20, default="n/a")
    vin_sticker = models.CharField(max_length=20, default="n/a")
    auction_id = models.IntegerField()
    year = models.IntegerField()
    model_name = models.CharField(max_length=20, default="n/a")
    mileage = models.IntegerField()
    unit_of_measurement = models.CharField(max_length=20, default="n/a")
    exterior_color = models.CharField(max_length=10, default="n/a")
    seller_name = models.CharField(max_length=20, default="n/a")
    purchase_date = models.DateTimeField(null=True)
    title_status = models.CharField(max_length=20, default="n/a")
    pdi_status = models.CharField(max_length=20, default="n/a")
    transport_status = models.CharField(max_length=20, default="n/a")
    location_name = models.CharField(max_length=20, default="n/a")
    buyer_rep_name = models.CharField(max_length=20, default="n/a")
    buyer_fee = models.CharField(max_length=20, default="n/a")
    buyer_ad_and_other_fees = models.CharField(max_length=20, default="n/a")
    fees_hst = models.CharField(max_length=20, default="n/a")
    taxable_purchase_price = models.CharField(max_length=20, default="n/a")
    total_hst = models.CharField(max_length=20, default="n/a")
    total_price = models.CharField(max_length=20, default="n/a")
    last_update_date_adesa = models.DateTimeField(null=True)
    last_update_date_gsm = models.DateTimeField(null=True)
    void_boolean = models.NullBooleanField(max_length=10)
    payment_status = models.CharField(max_length=10, default="n/a")
    amount = models.CharField(max_length=20, default="n/a")
    purchase_price = models.CharField(max_length=20, default="n/a")
    purchase_hst = models.CharField(max_length=20, default="n/a")
    bill_of_sale = models.URLField(default="n/a")
    checked = models.CharField(max_length=15, default="n/a")
    recalls = models.TextField(default="n/a")
    manufacturer_date = models.CharField(max_length=20, default="n/a")
    gvwr = models.CharField(max_length=20, default="n/a")
    gross_axle_weight_front = models.CharField(max_length=20, default="n/a")
    gross_axle_weight_rear = models.CharField(max_length=20, default="n/a")
    tire_size = models.CharField(max_length=20, default="n/a")
    tire_pressure_front = models.CharField(max_length=20, default="n/a")
    tire_pressure_rear = models.CharField(max_length=20, default="n/a")
    rim_size = models.CharField(max_length=20, default="n/a")
    adesa_id = models.CharField(max_length=20, default="n/a")


# totalLossCells, frameDamageCells, airbagCells, odometerCells, accidentCheckCells, recallCells
class CarFax(models.Model):
    vin = models.CharField(max_length=20)
    structural_damage = models.CharField(max_length=100, default="Check Online")
    total_loss = models.CharField(max_length=100, default="Check Online")
    accident = models.CharField(max_length=100, default="Check Online")
    airbags = models.CharField(max_length=100, default="Check Online")
    odometer = models.CharField(max_length=100, default="Check Online")
    recalls = models.CharField(max_length=100, default="Check Online")
    last_updated = models.DateTimeField(auto_now=True)  # updated timestamp
    html = models.TextField(blank=True, default="Check Online")
    origin_country = models.CharField(max_length=250, default="Check Online")
    run_date = models.CharField(max_length=20, default="Check Online")

class GetRecalls(models.Model):
    make = models.CharField(max_length=20, default="Check Online")
    vin = models.CharField(max_length=20)
    recalls = models.TextField(max_length=None, default="Check online")
    run_date = models.CharField(max_length=20, default="Check Online")



class GetAdesaRunList(models.Model):
    vin = models.CharField(max_length=20)
    img_url = models.URLField(blank=True)
    year = models.CharField(max_length=20, default="Check Online")
    make = models.CharField(max_length=20, default="Check Online")
    model = models.CharField(max_length=20, default="Check Online")
    grade = models.CharField(max_length=20, default="Check Online")
    colour = models.CharField(max_length=20, default="Check Online")
    MMR = models.TextField(default="n/a")
    run_date = models.CharField(max_length=20, default="Check Online")
    timestamp = models.DateTimeField(auto_now=True)  # updated timestamp
    lane = models.CharField(max_length=10, default="Check Online")
    trim = models.CharField(max_length=60, default="Check Online")
    mileage = models.CharField(max_length=20, default="Check Online")
    human_valuation = models.TextField(default="0")
    run_no = models.CharField(max_length=20, default="Check Online")
    adesa_id = models.CharField(max_length=20, default="n/a")
    engine = models.TextField(default="n/a")
    transmission = models.TextField(default="n/a")
    wheel_drive = models.CharField(max_length=50, default="n/a")
    interior_color = models.CharField(max_length=50, default="n/a")
    seller_announcements = models.TextField(default="n/a")
    auction_location = models.CharField(max_length=50, default="n/a")
    check = models.TextField(default="not available")
    extra = models.TextField(default="n/a")


    '''class Meta:
        ordering = ['id']'''

class DamageComparison(models.Model):
    id = models.BigIntegerField(default=0, max_length=None, primary_key=True)
    vin = models.CharField(max_length=20)
    year = models.CharField(max_length=20, default="Check Online")
    make = models.CharField(max_length=20, default="Check Online")
    model = models.CharField(max_length=20, default="Check Online")
    trim = models.CharField(max_length=60, default="Check Online")
    adesa_announcements = models.TextField(default="n/a")
    auction_location = models.CharField(max_length=50, default="n/a")
    carfax = models.TextField(default="n/a")
    BlackList = models.BigIntegerField(default=000, max_length=None)
    date = models.CharField(max_length=20, default="Check Online")
    analysis = models.TextField(default="n/a")
    adesa_id = models.TextField(default="n/a")

class ShoppingList(models.Model):
    vin = models.CharField(max_length=20)
    img_url = models.URLField(blank=True)
    year = models.CharField(max_length=20, default="Check Online", blank=True)
    make = models.CharField(max_length=20, default="Check Online", blank=True)
    model = models.CharField(max_length=20, default="Check Online", blank=True)
    grade = models.CharField(max_length=20, default="Check Online", blank=True)
    colour = models.CharField(max_length=20, default="Check Online", blank=True)
    MMR = models.TextField(default="n/a", blank=True)
    check = models.TextField(default="n/a", blank=True)
    run_date = models.CharField(max_length=20, default="Check Online")
    timestamp = models.DateTimeField(auto_now=True)  # updated timestamp
    lane = models.CharField(max_length=10, default="Check Online", blank=True)
    trim = models.CharField(max_length=60, default="Check Online", blank=True)
    mileage = models.CharField(max_length=20, default="Check Online", blank=True)
    human_valuation = models.TextField(default="0", blank=True)
    run_no = models.CharField(max_length=20, default="Check Online", blank=True)
    adesa_id = models.CharField(max_length=20, default="n/a", blank=True)
    engine = models.TextField(default="n/a", blank=True)
    transmission = models.TextField(default="n/a", blank=True)
    wheel_drive = models.CharField(max_length=50, default="n/a", blank=True)
    interior_color = models.CharField(max_length=50, default="n/a", blank=True)
    seller_announcements = models.TextField(default="n/a", blank=True)
    auction_location = models.CharField(max_length=50, default="n/a", blank=True)
    extra = models.TextField(default="n/a", blank=True)

    '''class Meta:
        ordering = ['id']'''


