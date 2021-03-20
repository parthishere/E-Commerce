from django.shortcuts import render, redirect

from products.models import Item
from .models import Cart

# Create your views here.
def cart_home(request):
    cart_obj = Cart.objects.new_or_get(request)
    context = {
    'objects' : cart_obj
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
        cart_obj = Cart.objects.new_or_get(request)
        if item_obj in cart_obj.item.all():
            cart_obj.item.remove(item_obj)
            cart_obj.save()
        else:
            cart_obj.item.add(item_obj)
            cart_obj.save()
    request.session['cart_item_number'] = cart_obj.item.count()
    return redirect('cart:cart-home') 