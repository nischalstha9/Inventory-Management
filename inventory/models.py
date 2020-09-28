from django.db import models
from django.urls import reverse
from django.utils.translation import gettext_lazy as _

class CommentManager(models.Manager):
    def all(self):
        qs = super(CommentManager, self).filter(parent = None)
        return qs

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length = 128, unique=True)
    parent = models.ForeignKey("self", null=True, blank=True, on_delete=models.SET_NULL)
    objects = CommentManager()

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
    name = models.CharField(max_length = 240, unique = True)
    brand = models.CharField(max_length = 50, null=True, blank=True)
    category = models.ForeignKey("inventory.Category", verbose_name=_("category"), on_delete=models.CASCADE)
    description = models.TextField(_(""))
    image = models.ImageField(_(""), upload_to="item_images", height_field=None, width_field=None, max_length=None, null=True, blank=True)
    cost_price = models.IntegerField(_(""))
    quantity = models.IntegerField(_(""))
    selling_price = models.IntegerField(_(""))
    about_seller = models.TextField(_(""))