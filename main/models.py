from django.db import models
from django.utils.translation import gettext_lazy as _
from accounts.models import User
# from django.utils import timezone
# from django.urls import reverse
# from django.db.models import Q
# from PIL import Image
# # Create your models here.

class SiteConfig(models.Model):
    key = models.CharField(_("Key"), max_length=50)
    value = models.CharField(_("Value"), max_length=50)

    class Meta:
        verbose_name = _("SiteConfig")
        verbose_name_plural = _("SiteConfigs")

    def __str__(self):
        return self.key

    def get_absolute_url(self):
        return reverse("SiteConfig_detail", kwargs={"pk": self.pk})

ORDER_STATUS = [
    ('NO', 'Not-Ordered'),
    ('O', 'Ordered'),
    ('C', 'Confirmed'),
    ('S', 'Fulfilled'),
]

class OrderItem(models.Model) :
    user = models.ForeignKey("accounts.User",verbose_name=_("Orderer"),on_delete=models.CASCADE)
    ordered = models.BooleanField(_("Is Ordered?"))
    item = models.ForeignKey("inventory.Item", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return f"{self.quantity} of {self.item.name}"

class Order(models.Model):
    user = models.ForeignKey("accounts.User", verbose_name=_("Orderer"), on_delete=models.CASCADE)
    items = models.ManyToManyField(OrderItem)
    ordered_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20,choices=ORDER_STATUS,default='NO')

    class Meta:
        verbose_name = _("Order")
        verbose_name_plural = _("Orders")

    def __str__(self):
        return f"Order By {self.user.email}"

    def get_absolute_url(self):
        return reverse("Order_detail", kwargs={"pk": self.pk})

    









# #database model for posts
# class PostManager(models.Manager):
#     def search(self, query=None):
#         qs = self.get_queryset()
#         if query is not None:
#             or_lookup = (Q(title__icontains=query, active=True) | 
#                          Q(content__icontains=query, active=True)
#                         )
#             qs = qs.filter(or_lookup).distinct() # distinct() is often necessary with Q lookups
#         return qs

# class BlogCategory(models.Model):
#     title=models.CharField(max_length=120)
#     def __str__(self):
#         return self.title

# class Post(models.Model):
#     title = models.CharField(max_length=100)
#     content = models.TextField()
#     date_posted= models.DateTimeField(auto_now_add=True)   #for adding date posted permanent
#     last_modified = models.DateTimeField(auto_now=True, blank=True)   #for adding date modified
#     author=models.ForeignKey(User, on_delete=models.CASCADE)
#     objects = PostManager()
#     likes = models.ManyToManyField(User, blank=True, related_name='post_likes')
#     category = models.ForeignKey(BlogCategory,on_delete=models.CASCADE, blank=True,null=True, related_name='categories')
#     active=models.BooleanField(blank=False, default=0)
#     cover_image=models.ImageField(blank=True,null=True,upload_to='blog_images')
#     youtube = models.CharField(max_length=1000,blank=True,null=True)
#     image_caption = models.CharField(blank=True,max_length=120)

#     def __str__(self):
#         return self.title

#     def get_absolute_url(self):
#         if self.active == True:
#             return reverse('post-detail',kwargs={'pk':self.pk })
#         else:
#             return reverse('user-drafts',kwargs={'username':self.author })

#     def get_like_url(self):
#         return reverse("post-like-toggle", kwargs={'pk':self.pk})
    
#     def save(self,*args,**kwargs):
#         super().save(*args,**kwargs)

#         if self.cover_image:
#             img = Image.open(self.cover_image.path)
#             if img.height > 1920 or img.width > 1920:
#                 output_size= (1920,1920)
#                 img.thumbnail(output_size)
#                 img.save(self.cover_image.path)