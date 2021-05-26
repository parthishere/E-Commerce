from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.utils.http import is_safe_url

from .forms import GuestForm
from .models import GuestEmail

# Create your views here.
def guest_register(request):
    form = GuestForm(request.POST or None)
    context = {
        "form": form
    }
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None
    if form.is_valid():
        email = form.cleaned_data.get('email')
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_id'] = new_guest_email.id
        
        if is_safe_url(redirect_path, request.get_host()):
            return redirect(redirect_path)
        else:
            return redirect("products:home")

    return redirect('products:home')