from django.db import models
from django.db.models.signals import pre_save, post_save, m2m_changed

from products.models import Item
from carts.models import Cart
from .utils import random_string_generator

ORDER_STATUS_CHOICES = (
    ('created', 'Created'),
    ('paid', 'Paid'),
    ('shipped', 'Shipped'),
    ('refunded', 'Refunded'),
)



def unique_id_generator(instance):
    """
    This is for a Django project and it assumes your instance 
    has a model order_id field
    """

    Klass = instance.__class__
    
    order_id = random_string_generator()
    
    qs_exists = Klass.objects.filter(order_id=order_id).exists()
    if qs_exists:
        new_order_id = random_string_generator()
        return unique_id_generator(instance)
    return order_id


# Create your models here.
class Order(models.Model):
    order_id 			= models.CharField(max_length=20)
    cart 				= models.ForeignKey(Cart, on_delete=models.CASCADE)
    status 				= models.CharField(choices=ORDER_STATUS_CHOICES, max_length=10, defaylt='created')
    shipping_total		= models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    order_total 		= models.IntegerField(default=0)
    shipping_address 	= models.TextField(blank=True, null=True)
    billing_address 	= models.TextField(blank=True, null=True)

    def __str__(self):
        return self.order_id

    def update_total(self):
        self.order_total = self.shipping_total + self.cart.total
        self.save()




def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        unique_id_generator(instance)

pre_save.connect(pre_save_create_order_id, sender=Order)

def post_save_order_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_id = instance.distinct()
        order_obj = Order.objects.filter(cart__id=cart_id)
        instance.update_total()

post_save.connect(post_save_order_total, sender=Cart)
	