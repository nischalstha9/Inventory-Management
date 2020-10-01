from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

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
    image = models.ImageField(_("Product Image"), upload_to="item_images", height_field=None, width_field=None, max_length=None, null=True, blank=True)
    cost_price = models.IntegerField(_("Cost Price"), default=0)
    quantity = models.IntegerField(_("Available Quantity"), default=0)
    selling_price = models.IntegerField(_("Selling Price"), default=0)
    about_seller = models.TextField(_("About Seller"))

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']

class DebitTransaction(models.Model):
    item = models.ForeignKey("inventory.Item", verbose_name=_("Inventory Item"), on_delete=models.CASCADE)
    seller = models.CharField(_("Seller Name or Company"), max_length=128)
    cost = models.IntegerField(_("Cost Price Per Quantity Unit"))
    paid = models.IntegerField(_("Paid Amount"), default = 0)
    sp = models.IntegerField(_("Selling Price"), default=0)
    quantity = models.IntegerField(_("Quantity"), default=0)
    remarks = models.TextField(_("Remarks on Deal"), null=True, blank=True)
    date = models.DateTimeField(_("Date Bought"), auto_now_add=True)

    def __str__(self):
        return f"{self.item} from {self.seller}"

    class Meta:
        ordering=["-date"]

    @property
    def remaining_payment(self):
        return self.cost*self.quantity - self.paid

    @property
    def total_payable(self):
        return self.cost*self.quantity

#rather than making Credit and Debit Transaction model use proxy mdoel and make 2 types
class CreditTransaction(models.Model):
    item = models.ForeignKey("inventory.Item", verbose_name=_("Inventory Item"), on_delete=models.CASCADE)
    buyer = models.CharField(_("Buyer Name or Company"), max_length=128)
    paid = models.IntegerField(_("Paid Amount"), default = 0)
    quantity = models.IntegerField(_("Quantity"), default=0)
    discount = models.FloatField(_("Discount Percentage"), default=0)
    remarks = models.TextField(_("Remarks on Deal"), null=True, blank=True)
    date = models.DateTimeField(_("Date Sold"), auto_now_add=True)

    def __str__(self):
        return f"{self.item} from {self.buyer}"

    class Meta:
        ordering=["-date"]

    @property
    def remaining_payment(self):
        p = (self.item.selling_price*self.quantity)
        return (p-self.discount/100*p) - self.paid

    @property
    def total_payable(self):
        p = (self.item.selling_price*self.quantity)
        return p-self.discount/100*p

    @property
    def sp(self):#selling_price
        return self.item.selling_price