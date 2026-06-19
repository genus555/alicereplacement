from django.contrib import admin
from .models.products import Products
from .models.category import Category
from .models.customer import Customer
from .models.orders import Order

admin.site.register(Products)
admin.site.register(Category)
admin.site.register(Customer)
admin.site.register(Order)