from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.validators import RegexValidator

class CategoryManager(models.Manager):
    def parents(self):
        qs = super(CategoryManager, self).filter(parent = None)
        return qs
    def childrens(self):
        qs = super(CategoryManager, self).filter(parent__isnull=False)
        return qs

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 128, unique=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    objects = CategoryManager()

    def __str__(self):
        return str(self.name)

    class Meta:
        ordering = ['name']
        verbose_name_plural = 'Categories'

    #replies
    def children(self):
        return Category.objects.filter(parent = self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    def get_absolute_url(self):
        return reverse('comment:thread',kwargs={'pk':self.pk })

    def get_api_url(self):
        return reverse('comment-api:comment-detail-api', kwargs ={'pk':self.pk})

class Item(models.Model):
    name = models.CharField(_("Product Name"),max_length = 240, unique = True)
    brand = models.CharField(_("Product Brand"), max_length = 50, null=True, blank=True)
    category = models.ForeignKey("inventory.Category", verbose_name=_("category"), on_delete=models.CASCADE, related_name='categories')
    description = models.TextField(_("Product Description"))
    image = models.ImageField(_("Product Image"), upload_to="product_images", height_field=None, width_field=None, max_length=None, null=True, blank=True)
    cost_price = models.FloatField(_("Latest Cost Price"), default=0)
    quantity = models.IntegerField(_("Available Quantity"), default=0)
    selling_price = models.FloatField(_("Current Selling Price"), default=0)
    about_seller = models.TextField(_("About Seller"))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class Transaction(models.Model):
    class Types(models.TextChoices):
        #TYPE_SNTX = TYPE_VALUE, TYPE_NAME
        STOCK_OUT = "STOCK OUT", "Stock Out"
        STOCK_IN = "STOCK IN", "Stock In"

    base_type = Types.STOCK_IN
    _type = models.CharField(
        _("Type"), max_length=50, choices=Types.choices, default=base_type
    )

    vendor_client = models.CharField(_("Vendor or Client"), max_length=240)
    item = models.ForeignKey("inventory.Item", verbose_name=_("Inventory Item"), on_delete=models.CASCADE)
    quantity = models.IntegerField(_("Quantity"), default=0)
    cost = models.FloatField(_("Cost Price Per Quantity Unit"), default=0)
    paid = models.FloatField(_("Paid Amount"), default = 0)
    remarks = models.TextField(_("Remarks on Deal"), null=True, blank=True)
    date = models.DateTimeField(_("Date of Transaction"), auto_now_add=True)
    balanced = models.BooleanField(_("Balanced"), editable = False)
    mobile_num_regex = RegexValidator(regex="^[0-9]{9,15}$", message="Entered mobile number isn't in a right format!")
    contact  = models.CharField(validators=[mobile_num_regex], max_length=13)

    class Meta:
        ordering = ['-date']

    def save(self, *args, **kwargs): 
        self.balanced = self.cost*self.quantity == self.paid
        super(Transaction, self).save(*args, **kwargs)

    def __str__(self):
        return f" {self.quantity} of {self.item}"

    @property
    def is_debit(self):
        return self._type == 'STOCK IN'

    @property
    def total_payable(self):
        return self.cost*self.quantity

    @property
    def remaining_payment(self):
        return self.total_payable - self.paid
    
    @property
    def unpaid(self):
        return self.remaining_payment > 0
    
    def get_absolute_url(self):
        return reverse("inventory:quick-payment", kwargs={"pk": self.pk})
    

class DebitTransactionManager(models.Manager):
    def unpaid(self):
        return self.get_queryset().filter(balanced=False)
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(_type=Transaction.Types.STOCK_IN)

class DebitTransaction(Transaction):
    base_type = Transaction.Types.STOCK_IN
    objects = DebitTransactionManager()

    class Meta:
        proxy = True

    # @property
    # def more(self):
    #     return self.debitInfo #here info is related with related name of transaction in DebitTransactionInfo Below


class CreditTransactionManager(models.Manager):
    def unpaid(self):
        return self.get_queryset().filter(balanced=False)
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(_type=Transaction.Types.STOCK_OUT)

class CreditTransaction(Transaction):
    base_type = Transaction.Types.STOCK_OUT
    objects = CreditTransactionManager()

    class Meta:
        proxy = True

    # @property
    # def more(self):
    #     return self.creditInfo #here info is related with related name of transaction in CreditTransactionInfo Below



#add payment model too it will be awesome
class Payment(models.Model):
    transaction = models.ForeignKey("inventory.Transaction", verbose_name=_("Payment For Transaction"), on_delete=models.CASCADE)
    amount = models.FloatField(_("Amount to add in Transaction"))
    date = models.DateField(_("Date of Payment"), auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.amount} for {self.transaction}"

# from django.db.models import F
# class DebitTransactionInfoManager(models.Manager):
#     def unpaid(self):
#         # return [i for i in DebitTransactionInfo.objects.all() if i.unpaid]
#         return self.annotate(remaining_payment = F('transaction__quantity')*F('cost')-F('transaction__paid'))
#     pass

# class DebitTransactionInfo(models.Model):
#     transaction = models.OneToOneField("inventory.DebitTransaction", verbose_name=_("info"), on_delete=models.CASCADE, related_name='debitInfo')
#     seller = models.CharField(_("Seller Name or Company"), max_length=128)
#     cost = models.IntegerField(_("Cost Price Per Quantity Unit"))
#     # remaining_payment = models.IntegerField(_("Remaining Payment"))
#     objects = DebitTransactionInfoManager()  

#     def save(self, *args, **kwargs): 
#         self.remaining_payment = self.cost*self.transaction.quantity - self.transaction.paid
#         super(DebitTransactionInfo, self).save(*args, **kwargs)

#     def __str__(self):
#         return f"Bought {self.transaction.item} from {self.seller}"

#     class Meta:
#         ordering=["-transaction__date"]

#     @property
#     def total_payable(self):
#         return self.cost*self.transaction.quantity

#     @property
#     def remaining_payment(self):
#         return self.total_payable - self.transaction.paid
    
#     @property
#     def unpaid(self):
#         return self.remaining_payment > 0


# #rather than making Credit and Debit Transaction model use proxy mdoel and make 2 types
# class CreditTransactionInfo(models.Model):
#     transaction = models.OneToOneField("inventory.CreditTransaction", verbose_name=_("info"), on_delete=models.CASCADE, related_name='creditInfo')
#     buyer = models.CharField(_("Buyer Name or Company"), max_length=128)
#     discount = models.FloatField(_("Discount Percentage"), default=0)

#     def __str__(self):
#         return f"Sold {self.transaction.item} to {self.buyer}"

#     class Meta:
#         ordering=["-transaction__date"]

#     @property
#     def remaining_payment(self):
#         p = (self.transaction.item.selling_price*self.transaction.quantity)
#         return (p-self.discount/100*p) - self.transaction.paid

#     @property
#     def total_payable(self):
#         p = (self.transaction.item.selling_price*self.transaction.quantity)
#         return p-self.discount/100*p

#     @property
#     def sp(self):#selling_price
#         return self.transaction.item.selling_price
