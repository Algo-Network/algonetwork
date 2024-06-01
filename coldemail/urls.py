
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("__reload__/", include("django_browser_reload.urls")),
    path('admin/', admin.site.urls),
    path('auth/', include('authentication.urls')),
    path('email/', include('sendingemail.urls')),
    path('email-data/', include('email_data.urls')),
    path('generator/', include('generator_message.urls')),
    path('', include('dashboard.urls')),
    
]
