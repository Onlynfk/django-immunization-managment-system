from django.shortcuts import render,redirect
from django.contrib.auth import authenticate
from django.urls import reverse
from django.http import HttpResponse, HttpResponseRedirect
from django.contrib.auth import logout, login
from django.contrib.auth.decorators import login_required



def home_page(request):
    return render(request,template_name='main.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(username=username, password=password)
        
        if user:
            if user.is_superuser:
                login(request,user)
                admin_url = redirect('admin-home')
                return admin_url
            elif user.is_hw:
                login(request,user)
                return HttpResponseRedirect(reverse('healthw-home'))
            elif user.is_pho:
                login(request,user)
                return HttpResponseRedirect(reverse('phealth-home'))
            else:
                print('Someone tried to login and failed')
                print("username: {} and password {}".format(username,password))
                return redirect('login')
        else:
                print('Someone tried to login and failed')
                print("username: {} and password {}".format(username,password))
                return redirect('login')
            
    else:
        return render(request, template_name='accounts/login.html', )
            
@login_required
def user_logout(request):
    logout(request)
    return redirect('main-home')

@login_required
def profile(request):
    return render(request, 'accounts/profile.html')
