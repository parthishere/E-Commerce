import math

from django.db import models
from django.shortcuts import reverse, redirect
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
        return unique_id_generator(instance)
    return order_id


class OrderManager(models.Manager):
    def new_or_get(self, cart_obj):
        # order_id = request.session.get('order_id', None)
        # cart_id = request.session.get('cart_id', None)
        # new_order_obj = False
        # qs = self.get_queryset().filter(id = order_id)
        # if qs is not None and qs.count==1:
        #     order_obj = qs.first()
        #     if request.user.is_authenticated and order_obj.cart is None:
        #         cart_obj, new_cart = Cart.objects.new_or_get(request)
        #         order_obj.cart = cart_obj
        #         print("Cart Added in Order")
        #         order_obj.save()
        # else:
        #     order_obj = self.new(request)
        #     print('new order created')
        #     request.session['order_id'] = order_obj.id
        #     new_order_obj = True
        created = False
        qs = self.get_queryset().filter(
                cart=cart_obj, 
                status='created'
            )
        if qs.count() == 1:
            obj = qs.first()
        else:
            obj = self.model.objects.create(
                    cart=cart_obj)
            created = True
        return obj, created
            
        return order_obj, new_order_obj
    
    def new(self, request):
        cart_id = request.session.get('cart_id', None)
        cart_obj = None
        if request.user.is_authenticated:
            cart_id = request.session.get('cart_id')
            cart_obj = Cart.objects.get(id=cart_id)
        return self.model.objects.create(cart=cart_obj)
        
            

# Create your models here.
class Order(models.Model):
    order_id 			= models.CharField(max_length=20)
    cart 				= models.ForeignKey(Cart, on_delete=models.CASCADE)
    status 				= models.CharField(choices=ORDER_STATUS_CHOICES, max_length=10, default='created')
    shipping_total		= models.DecimalField(max_digits=100, decimal_places=2, blank=True, null=True)
    order_total 		= models.DecimalField(decimal_places=2, max_digits=100, default=0.00)
    shipping_address 	= models.TextField(blank=True, null=True)
    billing_address 	= models.TextField(blank=True, null=True)

    objects = OrderManager()
    
    def __str__(self):
        return self.order_id

    def update_total(self):
        order_total = math.fsum([self.shipping_total + self.cart.total])
        self.order_total = format(order_total, '.2f')
        new_total = self.order_total
        self.save()
        return new_total




def pre_save_create_order_id(sender, instance, *args, **kwargs):
    if not instance.order_id:
        uq_id = unique_id_generator(instance)
        instance.order_id = uq_id

pre_save.connect(pre_save_create_order_id, sender=Order)

def post_save_cart_total(sender, instance, created, *args, **kwargs):
    if not created:
        cart_obj = instance
        cart_total = cart_obj.total
        cart_id = cart_obj.id
        qs = Order.objects.filter(cart__id=cart_id)
        if qs.count() == 1:
            order_obj = qs.first()
            order_obj.update_total()

post_save.connect(post_save_cart_total, sender=Cart)
	