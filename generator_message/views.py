from django.shortcuts import render

# Create your views here.
def generator_view(request):
    return render(request, "generator.html")
