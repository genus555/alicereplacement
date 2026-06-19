from django.shortcuts import render, redirect, HttpResponseRedirect
from store.models.products import Products
from store.models.category import Category
from django.views import View

class Index(View):
    def post(self, request):
        product = request.POST.get('product')
        remove = request.POST.get('remove')
        cart = request.session.get('cart')

        if cart:
            if remove:
                cart.pop(product, None)
            else:
                cart[product] = 1
        else:
            cart = {product: 1}
        request.session['cart'] = cart
        return redirect('homepage')
    
    def get(self, request):
        return HttpResponseRedirect(f'/store{request.get_full_path()[1:]}')

def store(request):
    cart = request.session.get('cart')
    if not cart:
        request.session['cart'] = {}
    products = None
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Products.get_all_products_by_categoryid(categoryID)
    else:
        products = Products.get_all_products()
    
    data = {}
    data['products'] = products
    data['categories'] = categories

    return render(request, 'index.html', data)