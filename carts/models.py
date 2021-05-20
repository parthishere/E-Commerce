from django.db import models
from django.conf import settings
from django.db.models.signals import pre_save, m2m_changed

from products.models import Item
# Create your models here.


class CartManager(models.Manager):
    def new_or_get(self, request):
        cart_id = request.session.get('cart_id', None)
        qs = self.get_queryset().filter(id=cart_id)
        user_model = None
        new_cart = False
        if qs.count() == 1 and qs.exists:
            cart_obj = qs.first()
            print("remeberd cart")
            if request.user.is_authenticated and cart_obj.user is None:
                cart_obj.user = request.user
                print("User added")
                cart_obj.save()
        else:
            cart_obj = self.new(user=request.user)
            print("new cart created")
            new_cart = True
            request.session['cart_id'] = cart_obj.id
        return cart_obj, new_cart   


    def new(self, user=None):
        user_model = None
        if user is not None and user.is_authenticated:
            user_model = user
        return self.model.objects.create(user=user_model)

    


class Cart(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)
    item = models.ManyToManyField(Item, blank=True)
    total = models.DecimalField(decimal_places=2, max_digits=100, default=0.00)
    

    objects = CartManager()

    def __str__(self):
        return str(self.id)

    

def m2m_changed_cart_reciever(sender, instance, action, *args, **kwargs):
	print(action)
	if action == 'post_add' or action == 'post_remove' or action == 'post_clear':
		products = instance.item.all()
		total = 0
		for x in products:
			total += x.price
		instance.total = total
		instance.save()

m2m_changed.connect(m2m_changed_cart_reciever, sender=Cart.item.through)

