import openai
import json
from decouple import config
import logging
from django.shortcuts import render
from django.http import StreamingHttpResponse, JsonResponse
from django.contrib.admin.views.decorators import staff_member_required

@staff_member_required(login_url='/auth/login/')
def generator_view(request):
    return render(request, "generator.html")
