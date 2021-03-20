from django.shortcuts import render
from django.views.generic import ListView
from products.models import Item
from tags.models import Tag
from django.db.models import Q


# Create your views here.
class SearchProductView(ListView):
    template_name = 'products/search-list.html'
    model=Item
    
    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        request = self.request
        query = request.GET.get('q')
        tags = Tag.objects.all()
        if query is not None:
            obj_list = (
                Q(title__icontains=query) | Q(text__icontains=query) | Q(tag__title__icontains=query)
            )
            context['object_list'] = Item.objects.filter(obj_list).distinct()
            context['query'] = query
            return context
        else:
            return Item.get_featured_item()
        
    
    
    