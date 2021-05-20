from django.urls import path, include
from .views import cart_home, cart_update, checkout_home



app_name = 'cart'


urlpatterns = [
    path('', cart_home, name='cart-home'),
    path('update/', cart_update, name='cart-update'),
    path('checkout', checkout_home, name='cart-checkout'),
    
]
