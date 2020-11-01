from django.contrib import admin
from .models import Item, Category, Transaction, DebitTransaction, CreditTransaction, Payment, Carousel, CarouselPhoto
from django.utils.translation import ugettext_lazy as _
from django_summernote.admin import SummernoteModelAdmin
from rangefilter.filter import DateRangeFilter, DateTimeRangeFilter


# Text to put at the end of each page's <title>.
admin.site.site_title = _('IMS')
# Text to put in each page's <h1> (and above login form)./ Tab heading
admin.site.site_header = _('Inventory Management System')
# Text to put at the top of the admin index page.
admin.site.index_title = _('Home Administration')


# Register your models here.
admin.site.register(Category)

# @admin.register(Item)
class ItemAdmin(SummernoteModelAdmin):
    search_fields = ['name', 'brand']
    list_display = ('name', 'category', 'cost_price', 'selling_price', 'quantity')
    list_filter = ('name', 'brand','category')
    readonly_fields = ('cost_price',)
    summernote_fields = ['description']

admin.site.register(Item, ItemAdmin)

class PaymentInline(admin.TabularInline):
    model = Payment
    fields = ('date', 'amount')
    readonly_fields = ['date']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    search_fields = ['item__name','vendor_client']
    list_display = ('vendor_client', 'date', 'item', 'quantity', 'contact', '_type', 'remaining_payment', 'balanced')
    list_editable = ['contact']
    list_filter = (('date', DateRangeFilter),'_type', 'item','vendor_client', 'balanced')
    readonly_fields = ('item','quantity','_type','remaining_payment','cost', 'paid')
    inlines = [
        PaymentInline,
    ]

@admin.register(DebitTransaction)
class DebitTransactionAdmin(TransactionAdmin):
    pass

@admin.register(CreditTransaction)
class CreditTransactionAdmin(TransactionAdmin):
    pass

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    search_fields = ['transaction__item','transaction__vendor_client']
    list_display = ('transaction', 'amount')
    readonly_fields = ('transaction', 'amount')
    list_filter = ('transaction__item', 'transaction__balanced')
  

class PhotoInline(admin.TabularInline):
    model= CarouselPhoto
    extra= 3

class CarouselAdmin(admin.ModelAdmin):
    inlines=[PhotoInline]
admin.site.register(Carousel, CarouselAdmin)
