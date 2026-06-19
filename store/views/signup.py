from django.shortcuts import render, redirect
from store.models.customer import Customer
from django.views import View

class Signup(View):
    def get(self, request):
        return render(request, 'signup.html')
    
    def post(self, request):
        ign = request.POST.get('ign')
        discord_name = request.POST.get('discord_name')
        value = {
            'ign': ign,
            'discord_name': discord_name,
        }
        error_message = None

        customer = Customer(ign=ign,
                            discord_name=discord_name)
        error_message = self.validateCustomer(customer)

        if not error_message:
            customer.discord_name = discord_name
            customer.register()
            return redirect('homepage')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'signup.html', data)
    
    def validateCustomer(self, customer):
        error_message = None
        if (not customer.ign):
            error_message = "Please enter your in game name."
        elif (not customer.discord_name):
            error_message = "Please enter your discord name."
        elif customer.isExists():
            error_message = "This in game name is already registered"
        return error_message