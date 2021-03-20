from django.urls import path, include
from .views import ProductListView, ProductDetailView, ContactUsView, CustomLogoutView, CustomSignUpView, CustomLogInView   



app_name = 'products'


urlpatterns = [
    path('products/', ProductListView.as_view(), name='list-cbv'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='detail-cbv'),
    path('contact-us/', ContactUsView.as_view(), name='contact-us'),
    path('products/<int:pk>', ProductDetailView.as_view(), name='detail-pk-cbv'),
    path('products/<slug:slug>', ProductDetailView.as_view(), name='detail-cbv'),
    path('accounts/logout', CustomLogoutView.as_view(), name='logout'),
    path('accounts/login', CustomLogInView.as_view(), name='login'),
    path('accounts/signup', CustomSignUpView.as_view(), name='signup'),
    
]
