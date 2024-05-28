from django.shortcuts import render

# Create your views here.
from django.contrib.auth.decorators import user_passes_test

@user_passes_test(lambda u: u.is_superuser, login_url='/auth/login/')
def generator_view(request):
    return render(request, "generator.html")
