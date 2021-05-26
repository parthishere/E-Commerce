from django.urls import path, include
from .views import guest_register



app_name = 'acc'


urlpatterns = [
    path('guest-register', guest_register, name='guest-login'),
    
    
]