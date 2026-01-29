from django.shortcuts import render
from django.views import View
from django .db.models import Q
from shop.models import Product

class SearchView(View):
    def get(self, request):
        query = request.GET.get('q')
        products = []
        if query:
            products = Product.objects.filter(
                Q(name__icontains=query) | Q(description__icontains=query) | Q(price__icontains=query)
            )
        context = {'products': products}
        return render(request, 'search.html', context)
