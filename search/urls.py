from django.urls import path, include
from .views import SearchProductView



app_name = 'search'


urlpatterns = [
    path('', SearchProductView.as_view(), name='search-cbv'),
    
]
