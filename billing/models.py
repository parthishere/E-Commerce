from django.db import models
from django.db.models.signals import post_save, pre_save

from django.contrib.auth.models import User

# Create your models here.

class BillingProfile(models.Model):
    user    = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    email = models.EmailField()
    active = models.BooleanField(null=True, blank=True, default=True)
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.email
    
def user_created_receiver(sender, instance, created, *args, **kwargs):
    if created:
        BillingProfile.objects.get_or_create(user=instance)
        
post_save.connect(user_created_receiver, sender=User)