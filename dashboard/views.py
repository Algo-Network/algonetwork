from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def home(request):
  return render(request, "Home.html")
