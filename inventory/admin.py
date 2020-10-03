from django.contrib import admin
from .models import Item, Category, Transaction, DebitTransaction, DebitTransactionInfo, CreditTransaction, CreditTransactionInfo, Payment
# Register your models here.
admin.site.register(Item)
admin.site.register(Category)
admin.site.register(Transaction)
admin.site.register(DebitTransaction)
admin.site.register(CreditTransaction)
admin.site.register(DebitTransactionInfo)
admin.site.register(CreditTransactionInfo)
admin.site.register(Payment)
