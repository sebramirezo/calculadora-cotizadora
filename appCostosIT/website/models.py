from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone

# Create your models here.
TIPO_LIC = [
    ('BBDD', 'BBDD'),
    ('Sistema Operativo', 'Sistema Operativo'),
]
LIC = [
    ('Red Hat', 'Red Hat'),
    ('MS Server', 'MS Server'),
]

class Licencia (models.Model):
    cod_lic = models.BigAutoField(primary_key=True)
    nom_lic = models.CharField(max_length=100)
    tipo_lic = models.CharField(max_length=100)
    costo_uf = models.FloatField(null=True)
    estado = models.BooleanField(default=1)

    def __str__(self):
        return self.nom_lic
    


SERVICIOS = [
    ('0', 'Sin Servicios Añadidos'),
    ('1', 'Redes y Seguridad'),
    ('2', 'Plataforma'),
    ('3', 'Base de Datos'),
    ('4', 'Integración'),
    ('5', 'Operaciones y Datacenter'),
    ('6', 'Operación de Aplicaciones'),
]

class Servicio (models.Model):
    cod_servicio = models.BigAutoField(primary_key=True)
    ## Campo nuevo
    nom_servicio_test = models.CharField(choices=SERVICIOS, max_length=45, default=SERVICIOS[0])
    ## Fin campo nuevo
    nom_servicio = models.CharField(max_length=45)
    valor_unit = models.FloatField(default=0)
    porcentaje = models.FloatField(default=100, null=True)
    user_crea = models.CharField(max_length=45, null=True)
    user_mod = models.CharField(max_length=45, null=True)
    fecha_crea = models.DateField(null=True)
    fecha_mod = models.DateField(null=True)
    estado = models.BooleanField(default=1)

    def __str__(self):
        return self.nom_servicio

class Recurso (models.Model):
    cod_rec = models.BigAutoField(primary_key=True)
    nom_rec = models.CharField(max_length=45)
    unidad = models.CharField(max_length=5, default=1)
    cantidad = models.IntegerField(default=1)
    valor_unit = models.FloatField(default=0)
    user_crea = models.CharField(max_length=45, null=True)
    user_mod = models.CharField(max_length=45, null=True)
    fecha_crea = models.DateField(null=True)
    fecha_mod = models.DateField(null=True)
    estado = models.BooleanField(default=1)


    def __str__(self):
        return self.nom_rec


class Servidor(models.Model):
    cod_serv = models.BigAutoField(primary_key=True)
    nom_serv = models.CharField(max_length=45)
    cant_serv = models.IntegerField(default=1)
    ambiente = models.CharField(max_length=4)
    user_crea = models.CharField(max_length=45, null=True)
    user_mod = models.CharField(max_length=45, null=True)
    fecha_crea = models.DateField(null=True)
    fecha_mod = models.DateField(null=True)
    estado = models.BooleanField(default=1)


    # Relaciones
    recursos = models.ManyToManyField(Recurso, through='servidor_has_recurso_edit')
    # licencias = models.ManyToManyField(Licencia)
    #servicios = models.ManyToManyField(Servicio)

    def __str__(self):
        return self.nom_serv

class servidor_has_recurso(models.Model):
    cod_serv = models.ForeignKey(Servidor, on_delete=models.CASCADE)
    cod_rec = models.ForeignKey(Recurso, on_delete=models.CASCADE)
    cantidad = models.IntegerField()
    valor = models.IntegerField()

    def __int__(self):
        return int(self.cod_serv)

#Integración de valores necesarios a servidor_has_recurso

class DdValues(models.Model):
    cod_value = models.BigAutoField(primary_key=True)
    label = models.IntegerField()

class RamValues(models.Model):
    cod_value = models.BigAutoField(primary_key=True)
    label = models.IntegerField()

class CpuValues(models.Model):
    cod_value = models.BigAutoField(primary_key=True)
    label = models.IntegerField()

# ddValues = [
#     ('1', 0),
#     ('2', 50),
#     ('3', 100),
#     ('4', 200),
#     ('5', 300),
#     ('6', 400),
#     ('7', 500),
#     ('8', 1000),
#     ('9', 2000),
#     ('10', 5000),
# ]

# cpuValues = [
#     ('1', 1),
#     ('2', 2),
#     ('3', 3),
#     ('4', 4),
#     ('5', 5),
#     ('6', 6),
#     ('7', 7),
#     ('8', 8),
#     ('9', 9),
#     ('10',10),
#     ('11',11),
#     ('12',12),
#     ('13',13),
#     ('14',14),
#     ('15',15),
#     ('16',16),
# ]

# ramValues = [
#     ('1',0),
#     ('2',1),
#     ('3',2),
#     ('4',4),
#     ('5',8),
#     ('6',16),
#     ('7',24),
#     ('8',32),
#     ('9',48),
#     ('10',64),
#     ('11',96),
#     ('12',112),
#     ('13',128),
# ]

get_ddValues = DdValues.objects.all()
ddValues = [(str(recurso.cod_value), recurso.label) for recurso in get_ddValues]

get_cpuValues= CpuValues.objects.all()
cpuValues = [(str(recurso.cod_value), recurso.label) for recurso in get_cpuValues]

get_ramValues = RamValues.objects.all()
ramValues = [(str(recurso.cod_value), recurso.label) for recurso in get_ramValues]

class servidor_has_recurso_edit(models.Model):
    cod_serv = models.ForeignKey(Servidor, on_delete=models.CASCADE, default=1)
    cod_rec = models.ForeignKey(Recurso, on_delete=models.CASCADE, default=1)
    dd_choice = models.CharField(choices=ddValues, default=100, max_length=45) #Etiqueta
    dd_valor = models.FloatField(default=0) #Valor
    cpu_choice = models.CharField(choices=cpuValues, default=4 ,max_length=45) #Etiqueta
    cpu_valor = models.FloatField(default=0) #Valor
    ram_choice = models.CharField(choices=ramValues, default=8, max_length=45) #Etiqueta
    ram_valor = models.FloatField(default=0) #Valor
    monto = models.IntegerField(default=0) #Suma valores

    def __int__(self):
        return (self.id)
    
class UFValue(models.Model):
    value = models.FloatField()
    last_updated = models.DateTimeField(auto_now=True)



    
##### Ejemplo de uso de servdor_has_recurso_edit
#1- Usuario elige en combobox el parametro que quiere para su servidor
#2- Usuario apreta botón Calcular estableciendo una petición POST al servidor (Debo ver como NO enviar esa info directamente al Servidor)
#3- El usuario visualizará en Detalle de Calculo el los valores con su respectivo monto total en UF y CLP
#   3.1- Este detalle requiere de que el botón calcular envie una redirección de los datos a menu_detalle.html.
#4- En la columna Detalle se requiere de un botón que establesca una petición a la base de datos y GUARDE el registro.
    