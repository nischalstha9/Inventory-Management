from django.contrib import admin
from .models import Item, Category, DebitTransaction
# Register your models here.
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(DebitTransaction)
