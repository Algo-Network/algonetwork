from django.shortcuts import render

# Create your views here.
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required(login_url='/auth/login/')
def generator_view(request):
    return render(request, "generator.html")
