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
            flag = check_password(discord_name, customer.discord_name)
            if flag:
                request.session['customer'] = customer.id
                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('homepage')
            else:
                error_message = 'In game name or Discord name invalid.'
        else:
            error_message = 'Invalid.'
        return render(request, 'login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')