from django.forms import ModelForm, ValidationError
from .models import *
from django import forms

get_ddValues = DdValues.objects.all()
ddValues = [(recurso.cod_value, recurso.label) for recurso in get_ddValues]

get_cpuValues= CpuValues.objects.all()
cpuValues = [(recurso.cod_value, recurso.label) for recurso in get_cpuValues]

get_ramValues = RamValues.objects.all()
ramValues = [(recurso.cod_value, recurso.label) for recurso in get_ramValues]

# ddValues = DdValues.objects.get('label', '')
# cpuValues = CpuValues.objects.get('label', '')
# ramValues = RamValues.objects.get('label', '')


# ddValues = [
#     (1, 0),
#     (2, 50),
#     (3, 100),
#     (4, 200),
#     (5, 300),
#     (6, 400),
#     (7, 500),
#     (8, 1000),
#     (9, 2000),
#     (10, 5000),
# ]

# cpuValues = [
#     (1, 1),
#     (2, 2),
#     (3, 3),
#     (4, 4),
#     (5, 5),
#     (6, 6),
#     (7, 7),
#     (8, 8),
#     (9, 9),
#     (10,10),
#     (11,11),
#     (12,12),
#     (13,13),
#     (14,14),
#     (15,15),
#     (16,16),

# ]

# ramValues = [
#     (1,0),
#     (2,1),
#     (3,2),
#     (4,4),
#     (5,8),
#     (6,16),
#     (7,24),
#     (8,32),
#     (9,48),
#     (10,64),
#     (11,96),
#     (12,112),
#     (13,128),
# ]
#
class ddValuesForm(ModelForm):

    class Meta:
        model = DdValues
        fields = '__all__'
#
class ramValuesForm(ModelForm):

    class Meta:
        model = RamValues
        fields = '__all__'
#
class CpuValuesForm(ModelForm):

    class Meta:
        model = CpuValues
        fields = '__all__'
#
TIPO_LIC = [
    ('BBDD', 'BBDD'),
    ('Sistema Operativo', 'Sistema Operativo'),
]
LIC = [
    ('Red Hat', 'Red Hat'),
    ('MS Server', 'MS Server'),
]
#
class LicenciaForm(ModelForm):
    # nom_lic = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-select m-2"}), choices=LIC)
    # tipo_lic =  forms.ChoiceField(widget=forms.Select(attrs={"class":"form-select m-2"}), choices=TIPO_LIC)

    class Meta:
        model = Licencia
        fields = ['cod_lic', 'nom_lic', 'tipo_lic', 'costo_uf']
#
class PorcentajeForm(forms.Form):
    porcentaje = forms.DecimalField(widget=forms.TextInput(attrs={"class":"form-control", "name":"porcentaje", "id":"porcentaje"}), required=False)

#
class ServicioForm(ModelForm):
    nom_servicio = forms.CharField()
    # porcentaje = forms.DecimalField(widget=forms.TextInput(attrs={"class":"form-control", "name":"porcentaje"}))
    # estado = forms.BooleanField(label='Checkbox')
    class Meta:
        model = Servicio
        fields = ['cod_servicio', 'nom_servicio', 'valor_unit', 'estado']
# 
class RecursoForm(ModelForm):
    class Meta:
        model = Recurso
        fields = ['cod_rec', 'nom_rec', 'valor_unit', 'unidad', 'cantidad']
# 
class ServidorForm(ModelForm):
    nom_serv = forms.CharField(widget=forms.TextInput(attrs={"class":"form-control", "placeholder": "Ingresa un nombre"}), label='')
    cant_serv = forms.IntegerField(widget=forms.NumberInput(attrs={"class":"form-control", "placeholder":"Ingresa cantidad de servidores"}), label='')
    
    class Meta:
        model = Servidor
        fields = ['nom_serv', 'cant_serv']
# 
#Clase que crea formularios de elección de etiquetas
class MyForm(forms.Form):
    dd_choice = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-select m-2"}), choices=ddValues)
    ram_choice = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-select m-2"}), choices=ramValues)
    cpu_choice = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-select m-2"}), choices=cpuValues)

##Bard##
class servidor_has_recurso_editForm(ModelForm):
    dd_choice = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-select m-2", "aria-label":"Selección de disco duro"}), choices=ddValues)
    ram_choice = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-select m-2", "aria-label":"Selección de memoria ram"}), choices=ramValues)
    cpu_choice = forms.ChoiceField(widget=forms.Select(attrs={"class":"form-select m-2", "aria-label":"Selección de cpu"}), choices=cpuValues)

    class Meta:
        model = servidor_has_recurso_edit
        fields = ['dd_choice', 'cpu_choice', 'ram_choice']
#
class UFValueForm(ModelForm):
    value = forms.FloatField(widget=forms.NumberInput(attrs={"class":"form-control", "placeholder":"Ingresa UF", 'id':'value'}), label='', required=True)

    class Meta:
        model = UFValue
        fields = ['value']