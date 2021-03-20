from django.db import models

from products.models import Item

# Create your models here.
class Order(models.Model):
	item = models.ManyToManyField(Item)
	# order_id
	# address
	