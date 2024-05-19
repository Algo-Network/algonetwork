from django.urls import path
from .views import postsignIn, logout, signIn

app_name = 'authentication'


urlpatterns = [
    path('auth/', postsignIn, name='auth'),
    path('logout/', logout, name='logout'),
    path('', signIn, name='login'),
]