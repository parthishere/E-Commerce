from django.db import models
from django.db.models.signals import post_save, pre_save

from django.contrib.auth.models import User

# Create your models here.
class BillingManager(models.Manager):
    def new_or_get(self, request, email):
        user = request.user
        created = False
        qs = self.get_queryset().filter(user=user)
        if qs.exists():
            order_obj = qs.first()
        else:
            order_obj = self.new(request=request, email=email)
            created = True
        return order_obj, created 
    
    def new(self, request, email):
        if request.user.is_authenticated:
            self.model.objects.create(user=request.user, email=email)
            


class BillingProfile(models.Model):
    user    = models.OneToOneField(User, on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(null=True, blank=True, default=True)
    timestamp = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    update = models.DateTimeField(auto_now=True)
    
    objects = BillingManager()
    
    def __str__(self):
        return self.email
    
def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        BillingProfile.objects.get_or_create(user=instance)
        
post_save.connect(user_created_receiver, sender=User)