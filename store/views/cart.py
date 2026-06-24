from django.shortcuts import render
from django.views import View
from store.models.products import Products

class Cart(View):
    def get(self, request):
        products = Products.get_products_by_id(list(request.session.get('cart').keys()))
        total_price = Products.get_products_price_total(products)
        return render(request, 'cart.html', {'products': products,
                                             'total_price': total_price
                                             })