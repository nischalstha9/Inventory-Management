from django.contrib import admin
from .models import SiteConfig, OrderItem, Order
# Register your models here.
admin.site.register(SiteConfig)
admin.site.register(OrderItem)
admin.site.register(Order)
