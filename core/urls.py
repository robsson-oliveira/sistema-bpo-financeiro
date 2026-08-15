from django.contrib import admin
from django.urls import path, include
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


@login_required
def home_temporaria(request):
    return HttpResponse(f"Logado como: {request.user.username} ({request.user.email})")


urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('allauth.urls')),
    path('', home_temporaria),
]