from django.contrib import admin
from .models import *

# Register your models here.
admin.site.register(Servicio)
admin.site.register(Licencia)
admin.site.register(Recurso)
admin.site.register(Servidor)
admin.site.register(servidor_has_recurso)
admin.site.register(servidor_has_recurso_edit)
admin.site.register(UFValue)