from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.products import Products
from store.models.orders import Order

class CheckOut(View):
    def post(self, request):
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Products.get_products_by_id(list(cart.keys()))

        for product in products:
            order = Order(customer_id=customer,
                          product=product,
                          price=product.price,
                          )
            order.save()
        request.session['cart'] = {}

        return redirect('cart')