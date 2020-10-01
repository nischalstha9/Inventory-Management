from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

# Create your models here.
class Invoice(models.Model):
    buyer_name = models.CharField(_("Buyer's Name"), max_length=128)
    date_created = models.DateTimeField(_("Date"), auto_now_add=True)

    class Meta:
        ordering = ['-date_created']

    def __str__(self):
        return self.buyer_name

    def get_items(self):
        return self.MainInvoice.all()

    def get_items_variety_count(self):
        return self.MainInvoice.all().count()

    def get_total_of_items(self):
        return sum([(i.sp*i.quantity) for i in self.MainInvoice.all()])

class InvoiceItem(models.Model):
    invoice = models.ForeignKey("invoice.Invoice", verbose_name=_("Invoice"), on_delete=models.CASCADE, related_name = "MainInvoice")# we will use main invoice to get all invoice_items of parent invoice object
    item = models.ForeignKey("inventory.Item", verbose_name=_("Item Name"), on_delete=models.CASCADE)
    quantity = models.IntegerField(_("Quantity"))
    sp = models.IntegerField(_("Selling Price / Quantity"))
    #use disount instead of sp tat way you idiot can use default selling_price

    def __str__(self):
        return f"{self.invoice} => {self.item}"

    @property
    def total(self):
        return self.quantity * self.sp