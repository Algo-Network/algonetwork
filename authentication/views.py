from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

def login_user(request):
    if request.user.is_authenticated:
        return redirect('dashboard:home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if user.is_staff or user.is_superuser:
                login(request, user)
                return redirect('dashboard:home')
            else:
                messages.error(request, 'Access restricted to admin users only.')
        else:
            messages.error(request, 'The username or password is incorrect!')
    context = {}
    return render(request, 'login.html', context)

@login_required(login_url='/login/')
def logout_user(request):
    logout(request)
    return redirect('authentication:login')
