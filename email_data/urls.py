from django.urls import path
from . import views

app_name = 'email_data'

urlpatterns = [
    path('', views.email_list, name='email_list'),
    path('email/new/', views.email_create, name='email_create'),  # Pastikan URL pattern untuk create ada di sini
    path('email/<str:email>/', views.email_detail, name='email_detail'),
    path('email/<str:email>/edit/', views.email_update, name='email_update'),
    path('email/<str:email>/delete/', views.email_delete, name='email_delete'),
]
