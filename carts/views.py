from accounts.models import GuestEmail
from django.http.response import Http404
from django.shortcuts import render, redirect, reverse

from products.models import Item
from billing.models import BillingProfile
from orders.models import Order
from .models import Cart
from accounts.forms import GuestForm
from allauth.account.forms import LoginForm

# Create your views here.
def cart_home(request):
    cart_obj, new_cart = Cart.objects.new_or_get(request)
    context = {
    'cart' : cart_obj
    }
    return render(request, 'carts/cart.html', context=context)


def cart_update(request):
    product_id = request.POST.get('product_id')
    print(product_id)
    if product_id is not None:
        try:
            item_obj = Item.objects.get(id=product_id)	    
        except:
            print("Show massage that object does not exist!")
            return redirect('cart:cart-home')
        cart_obj, new_cart = Cart.objects.new_or_get(request)
        if item_obj in cart_obj.item.all():
            cart_obj.item.remove(item_obj)
            cart_obj.save()
        else:
            cart_obj.item.add(item_obj)
            cart_obj.save()
        request.session['cart_item_number'] = cart_obj.item.count()
    return redirect('cart:cart-home') 


def checkout_home(request):
    cart_obj, new_cart = Cart.objects.new_or_get(request)
    order_obj = None
    if not new_cart or cart_obj.item.count != 0:
        order_obj, new_order_obj = Order.objects.new_or_get(cart_obj)
    else:
        return redirect('cart:home')
    
    user = request.user
    biling_profile = None
    login_form = LoginForm()
    guest_form = GuestForm()
    guest_email_id =request.session.get('guest_id')
    
    if user.is_authenticated:
        billing_profile = BillingProfile.objects.new_or_get(request, email=user.email)
    
    elif guest_email_id is not None:
        guest_email_obj = GuestEmail.objects.get(id=guest_email_id)
        billing_profile = BillingProfile.objects.new_or_get(email=guest_email_obj.email)
        
    else:
        print('nothing found')
    
    context = {
        'object': order_obj,
        'billing_profile': billing_profile,
        'form': login_form,
        'guest_form': GuestForm,
    }
    return render(request, 'carts/checkout.html', context=context)