from django.shortcuts import render, redirect, reverse
from django.views.generic import (
    CreateView,
    TemplateView,
    ListView,
    DeleteView, 
    DetailView, 
    UpdateView
)
from .models import Item
from carts.models import Cart
# Create your views here.


'''

Unlike in function based views where http methods are evaluated 
in a conditional branching statements,Class Based Views handle each 
request type in a distinct class instance method named correspondingly
to the request method.Example, the get() method handles GET request
and the post() method handles POST requests.

def get(self, request, *args, **kwargs):
          form = self.form_class(initial=self.initial)
          return render(request, self.template_name, {'form': form})

      def post(self, request, *args, **kwargs):
          form = self.form_class(request.POST)
          if form.is_valid():
              # <process form cleaned data>
              return HttpResponseRedirect('/success/')
          return render(request, self.template_name, {'form': form})        

'''




class ProductListView(ListView):
    template_name = 'products/item-list.html'
    model = Item

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        return context


class ProductDetailView(DetailView):
    template_name = 'products/product-detail.html'
    model = Item

    def get_context_data(self, *args, **kwargs):
        context = super(ProductDetailView, self).get_context_data(*args, **kwargs)
        request = self.request
        context['cart'] = Cart.objects.new_or_get(request)
        return context
    


class ContactUsView(TemplateView):
    template_name = 'products/contact_us.html'



######################################################################################################################################33



from allauth.account.views import LogoutView, LoginView, SignupView
from django.shortcuts import reverse
from django.urls import reverse_lazy


class CustomLogoutView(LogoutView):
    success_url = reverse_lazy('products:list-cbv')
    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form.

        Using this instead of just defining the success_url attribute
        because our url has a dynamic element.
        """
        
        next_ = self.request.POST.get('next')
        next_get = self.request.GET.get('next')
        
        next_ = next_ or next_get
        if next_ is not None:
            return next_
        else:
            return self.success_url


class CustomLogInView(LoginView):
    success_url = reverse_lazy('products:list-cbv')
    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form.

        Using this instead of just defining the success_url attribute
        because our url has a dynamic element.
        """
        next_ = self.request.POST.get('next')
        next_get = self.request.GET.get('next')
        
        next_ = next_ or next_get
        if next_ is not None:
            return next_
        else:
            return self.success_url



class CustomSignUpView(SignupView):
    success_url = reverse_lazy('products:list-cbv')
    def get_success_url(self):
        """
        Return the URL to redirect to after processing a valid form.

        Using this instead of just defining the success_url attribute
        because our url has a dynamic element.
        """
        
        next_ = self.request.POST.get('next')
        next_get = self.request.GET.get('next')
        print(next_)
        next_ = next_ or next_get
        if next_ is not None:
            return next_
        else:
            return self.success_url