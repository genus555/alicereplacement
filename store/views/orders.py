from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password
from store.models.customer import Customer
from django.views import View
from store.models.products import Products
from store.models.orders import Order
import logging

logger = logging.getLogger('django')

class OrderView(View):
    def post(self, request):
        order_id = request.POST.get('order')
        remove = request.POST.get('remove')
        current_customer_id = request.session.get('customer')
        try:
            order = Order.objects.get(id=order_id)
        except Order.DoesNotExist:
            logger.warning(f"Trying to remove an order that doesn't exist. False Order ID {order_id}")
            return redirect('orders')
        
        customer_id = order.customer_id

        if customer_id == current_customer_id:
            if remove:
                order.delete()
                logger.debug(f"Order {order_id}: {order} | "
                             f"This order has been successfully deleted."
                             )
                return redirect('orders')
        else:
            current_customer = Customer.objects.get(id=current_customer_id)
            customer = Customer.objects.get(id=customer_id)
            logger.warning(f"Wrong customer removing order. | "
                           f"Current Customer: {current_customer.ign} {current_customer.discord_name} | "
                           f"Order's Customer: {customer.ign} {customer.discord_name}"
                           f"Order: {order}"
                           )
            return redirect('homepage')

    def get(self, request):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        return render(request, 'orders.html', {
            'orders': orders,
            'customer': customer
            })