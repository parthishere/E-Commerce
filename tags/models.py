from django.db import models
from products.models import Item
from django.utils.text import slugify




class Tag(models.Model):
    title     = models.CharField(max_length=120)
    slug      = models.SlugField()
    products  = models.ManyToManyField(Item, blank=True)
    active    = models.BooleanField(default=True)

    def __str__(self):
        return self.title

    # def save(self, *args, **kwargs):
    #     value = self.title
    #     self.slug = slugify(value, allow_unicode=True)
    #     super().save(*args, **kwargs)
