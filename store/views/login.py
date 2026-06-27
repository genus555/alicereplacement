from django.shortcuts import render, redirect, HttpResponseRedirect
from django.views import View
from store.models.customer import Customer
import logging

logger = logging.getLogger('django')

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
                logger.info(f"Login sucessful: IGN: \"{discord_name}\" | Discord Name: \"{ign}\"")
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_message = 'IGN or Discord name is incorrect.'
                logger.warning(f"Login Discord Name Wrong. Attempted Values: IGN: \"{discord_name}\" | Discord Name: \"{ign}\"")
        else:
            error_message = 'Invalid'
            logger.warning(f"Login Invalid. Attempted Values: IGN: \"{discord_name}\" | Discord Name: \"{ign}\"")
        
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