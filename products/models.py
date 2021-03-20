from django.db import models
from django.shortcuts import reverse
from django.utils.text import slugify
from django.db.models.signals import pre_save, post_save

from .utils import random_string_generator





CATEGORY_CHOICES = [
    ('S', 'SHIRT'),
    ('TS', 'T-SHIRT'),
    ('P', 'PANTS'),

]


def unique_slug_generator(instance, new_slug=None):
    """
    This is for a Django project and it assumes your instance 
    has a model with a slug field and a title character (char) field.
    """
    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exists()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                )
        return unique_slug_generator(instance, new_slug=new_slug)
    return slug


class Item(models.Model):
    image = models.ImageField(upload_to='products/',null=True, blank=True)
    title = models.TextField(max_length=50)
    text  = models.TextField()
    slug = models.SlugField()
    price = models.FloatField()
    dis_price = models.FloatField() 
    timestamp = models.DateTimeField(auto_now_add=True)
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("products:detail-cbv", kwargs={"slug": self.slug})
    
    def get_featured_item(self):
        return self.objects.filter(title__icontains='wallpaper')

    # def save(self, *args, **kwargs):
    #     value = self.title
    #     self.slug = slugify(unique_slug_generator(instance), allow_unicode=True)
    #     super().save(*args, **kwargs)
    
def product_pre_save_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

pre_save.connect(product_pre_save_receiver, sender=Item)