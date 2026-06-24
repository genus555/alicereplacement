from django.db import models
from .products import Products
from .customer import Customer
import datetime

class Order(models.Model):
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    price = models.IntegerField()
    date = models.DateField(default=datetime.date.today)
    status = models.BooleanField(default=False)

    def placeOrder(self):
        self.save()

    @staticmethod
    def get_orders_by_customer(customer_id):
        return Order.objects.filter(customer=customer_id).order_by('-date')
    
    class Meta:
        verbose_name_plural = "Orders"

    def __str__(self):
        return f"\"{self.customer.ign}\" asked for: {self.product.category} {self.product.name}"