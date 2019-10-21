# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from api.models import GetRecalls, GetAdesaPurchases, CarFax, GetAdesaRunList, ShoppingList

# Register your models here.
admin.site.register(GetRecalls)
admin.site.register(GetAdesaPurchases)
admin.site.register(CarFax)
admin.site.register(GetAdesaRunList)
admin.site.register(ShoppingList)
