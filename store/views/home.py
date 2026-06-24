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

        return_url = request.GET.get('return_url')
        if return_url:
            return redirect(return_url)
        
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
    search_query = request.GET.get('search')
    current_category = None  
    if categoryID:
        products = Products.get_all_products_by_categoryid(categoryID)
        try:
            category_obj = Category.objects.get(id=categoryID)
            current_category = category_obj.name.lower()
        except Category.DoesNotExist:
            pass
    else:
        products = Products.get_all_products()

    if search_query:
        products = products.filter(name__icontains=search_query)
    
    data = {}
    data['products'] = products
    data['categories'] = categories
    data['current_category'] = current_category

    return render(request, 'index.html', data)