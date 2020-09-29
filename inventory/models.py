from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class CategoryManager(models.Manager):
    def parents(self):
        qs = super(CategoryManager, self).filter(parent = None)
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
    cost_price = models.IntegerField(_("Cost Price"))
    quantity = models.IntegerField(_("Available Quantity"))
    selling_price = models.IntegerField(_("Selling Price"))
    about_seller = models.TextField(_("About Seller"))

    def __str__(self):
        return self.name