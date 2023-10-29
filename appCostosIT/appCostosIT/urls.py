
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    #Esta url permite tener acceso al django admin y sus funciones
    path('admin/', admin.site.urls),
    #Esta url tambien permite tener el control de usuarios mediante django auth
    path('accounts/', include('django.contrib.auth.urls')),
    #Esta url pertenece a las que se especifican en urls.py del website
    path('', include('website.urls')),
]