from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from store.models.customer import Customer
from django.contrib.auth.hashers import check_password

class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request, 'login.html')
    
    def post(self, request):
        ign = request.POST.get('ign')
        discord_name = request.POST.get('discord_name')
        customer = Customer.get_customer_by_in_game_name(ign)
        error_message = None
        if customer:
            if discord_name == customer.discord_name:
                request.session['customer'] = customer.id
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_message = 'IGN or Discord name is incorrect.'
        else:
            error_message = 'Invalid'
        
        value = {
            'ign': ign,
            'discord_name': discord_name,
        }
        return render(request, 'login.html', {
            'error': error_message,
            'values': value
            })

def logout(request):
    request.session.clear()
    return redirect('homepage')