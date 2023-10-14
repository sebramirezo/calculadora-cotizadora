import logging
from django.contrib import messages
from django.shortcuts import redirect, render
from .models import *
from .forms import *
from .uf import *
from datetime import date
from django.contrib.auth import logout
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, permission_required


def redirect_login(request):
    return redirect('login')

class CustomLoginView(LoginView):
    template_name = 'registration/login.html'

def cerrar_sesion(request):
    logout(request)
    return redirect('/login')

def error_404_view(request):
    return render(request, '404.html', status=404)

    ##############
## Vista principal ##
    ##############
# @login_required
def index(request):
    # Almacenar los resultados de las funciones en variables
    resultado_dd = getResultDD(request)
    resultado_cpu = getResultCpu(request)
    resultado_ram = getResultRam(request)
    resultado_suma = getSumMonto(request)
    resultado_total = getSumMonto_CLP(request)
    dd_values_count = DdValues.objects.count()
    ram_values_count = RamValues.objects.count()
    cpu_values_count = CpuValues.objects.count()
    fecha_actual = date.today()
    list_servicios = Servicio.objects.all()
    list_licencias = Licencia.objects.all()
    form_servicios = ServicioForm()
    form = servidor_has_recurso_editForm()
    form_nom = ServidorForm()
    form_licencias = LicenciaForm()
    form_uf = 0
    uf_value = 0
    cant_serv = 1
    # porcentaje = 0
    valor_unit_p = 1
    form_uf = UFValueForm()

    if request.method == 'POST':
        form = servidor_has_recurso_editForm(request.POST)
        form_nom = ServidorForm(request.POST)
        form_servicios = ServicioForm(request.POST)
        nom_serv = request.POST.get('nom_serv')
        cant_serv = request.POST.get('cant_serv')
        porcentaje = request.POST.get('porcentaje')
        porcentaje = float(porcentaje)
        list_servicios.update(porcentaje=porcentaje)
        form_licencias = LicenciaForm(request.POST)
        form_uf = UFValueForm(request.POST)
        uf_value = request.POST.get('value')

        boxes = request.POST.getlist('boxes')
        boxes_int = [int(box) for box in boxes]
        servicios_dict = {servicio.cod_servicio: servicio.valor_unit for servicio in list_servicios}
        servicios_dict_nombres = {servicio.cod_servicio: servicio.nom_servicio for servicio in list_servicios}
        valores = []
        list_servicios.update(estado=False)
        # list_servicios.update(porcentaje=0)

        # Obtén el porcentaje del formulario
        # porcentaje = request.POST.get('porcentaje')
        # porcentaje = float(porcentaje)

        for box in boxes_int:
            valor = servicios_dict.get(box, 'Valor no encontrado')
            nombre = servicios_dict_nombres.get(box, 'Nombre no encontrado')
            
            porcentaje_en_dec = (1 - (porcentaje / 100))
            valor_unit_p = valor * porcentaje_en_dec
            print(valor_unit_p)
            valores.append((nombre, int(valor_unit_p)))
            Servicio.objects.filter(pk=int(box)).update(estado=True)

        boxes_lic = request.POST.getlist('boxes_lic')
        boxes_int_lic = [int(box1) for box1 in boxes_lic]
        licencias_dict = {licencia.cod_lic: licencia.costo_uf for licencia in list_licencias}
        licencias_dict_nombres = {licencia.cod_lic: licencia.nom_lic for licencia in list_licencias}
        valores_lic = []
        list_licencias.update(estado=False)
        for box1 in boxes_int_lic:
            valor = licencias_dict.get(box1, 'Valor no encontrado')
            nombre = licencias_dict_nombres.get(box1, 'Nombre no encontrado')
            valores_lic.append((nombre, int(valor)))
            Licencia.objects.filter(pk=int(box1)).update(estado=True)

        print('EStos son los valores lix ' + str(valores_lic))
        print(boxes)
        print(valores)

        if form.is_valid():
            # Validar datos
            logging.info('Form validado')
            # Obtener la etiqueta de dd_choice, cpu_choice y ram_choice
            dd_choice_label = form.instance.get_dd_choice_display()
            cpu_choice_label = form.instance.get_cpu_choice_display()
            ram_choice_label = form.instance.get_ram_choice_display()

            # Puedes usar estas etiquetas para almacenarlas en la base de datos
            form.instance.dd_choice = dd_choice_label
            form.instance.cpu_choice = cpu_choice_label
            form.instance.ram_choice = ram_choice_label
            print(dd_choice_label)
            print(cpu_choice_label)
            print(ram_choice_label)


            form.save(commit=False)
            if 'btnGuardar' in request.POST:
                instancia = form.save(commit=False)
                instancia.save()
                return redirect('/')

            # Crear un contexto para pasar los datos a la plantilla
            context = {
                'form': form,
                'form_nom': form_nom,
                'nom_servidor': nom_serv,
                'cant_serv':cant_serv,
                'form_servicios':form_servicios,
                'porcentaje':porcentaje,
                'form_licencias':form_licencias,
                'form_uf':form_uf,
                'value': uf_value,
                'fecha_actual':fecha_actual,
                'dd_choice_label':dd_choice_label,
                'cpu_choice_label':cpu_choice_label,
                'ram_choice_label':ram_choice_label,
                'resultado_dd': resultado_dd,
                'resultado_cpu': resultado_cpu,
                'resultado_ram': resultado_ram,
                'dd_values_count':dd_values_count,
                'ram_values_count':ram_values_count,
                'cpu_values_count':cpu_values_count,
                'suma': resultado_suma,
                'total': resultado_total,
                'list_servicios': list_servicios,
                'list_licencias':list_licencias,
                'boxes':boxes_int,
                'boxes_lic':boxes_lic,
                'servicios_dict':servicios_dict,
                'valores':valores,
                'valores_lic':valores_lic,
                'errors': form.errors.as_text()
            }

            return render(request, 'plantilla.html', context)
        else:
            # Crear un contexto para pasar los datos a la plantilla
            context = {
                'form': form,
                'form_nom': form_nom,
                'porcentaje':porcentaje,
                'cant_serv':cant_serv,
                'form_uf':form_uf,
                'value': uf_value,
                'dd_values_count':dd_values_count,
                'ram_values_count':ram_values_count,
                'cpu_values_count':cpu_values_count,
                'form_servicios':form_servicios,
                'form_licencias':form_licencias,
                'list_servicios': list_servicios,
                'list_licencias':list_licencias,
                'errors': form.errors.as_text()
            }

            return render(request, 'plantilla.html', context)
    else:
        # Crear un contexto para pasar los datos a la plantilla
        context = {
            'form': form,
            'form_nom': form_nom,
            'porcentaje':porcentaje,
            'cant_serv':cant_serv,
            'form_uf':form_uf,
            'value': uf_value,
            'dd_values_count':dd_values_count,
            'ram_values_count':ram_values_count,
            'cpu_values_count':cpu_values_count,
            'form_servicios':form_servicios,
            'form_licencias':form_licencias,
            'list_servicios': list_servicios,
            'list_licencias':list_licencias,
            'errors': form.errors.as_text()
        }

        return render(request, 'plantilla.html', context)
    
    ##################################
    ##  Vista de Mantenedor Recurso ##
    ##################################
@login_required
def mantenedorRecurso(request):
    recursos = Recurso.objects.all()
    context = {
        'recursos':recursos
    }
    return render(request, 'mantenedor_recursos.html', context)

@login_required
def edicionRecurso(request, cod_rec):
    recursos = Recurso.objects.get(cod_rec=cod_rec)
    context = {
        'recursos':recursos
    }
    return render(request, 'edicionRecurso.html', context)

@login_required
def editarRecurso(request):
    cod_rec = request.POST.get('cod_rec')
    nom_rec = request.POST.get('nom_rec')
    valor_unit = request.POST.get('valor_unit')

    recursos_get = Recurso.objects.get(cod_rec=cod_rec)

    recursos_get.nom_rec = nom_rec
    recursos_get.valor_unit = valor_unit

    recursos_get.save()
    return redirect('/mantenedor_recursos')

    ##################################
    ##  Vista de Mantenedor Servicio ##
    ##################################

@login_required
def mantenedorServicio(request):
    servicios = Servicio.objects.all()
    context = {
        'servicios':servicios
    }
    return render(request, 'mantenedor_servicios.html', context)

@login_required
def registrarServicio(request):
    # cod_servicio = request.POST('cod_servicio')
    # nom_servicio = request.POST('nom_servicio')
    # valor_unit = request.POST('valor_unit')

    form_reg_servicio = ServicioForm()

    if request.method == 'POST':
        form_reg_servicio = ServicioForm(request.POST)
        if form_reg_servicio.is_valid():

            max_cod = Servicio.objects.aggregate(models.Max('cod_servicio'))['cod_servicio__max']
            nuevo_cod = max_cod + 1

            servicio = form_reg_servicio.save(commit=False)
            servicio.cod = nuevo_cod
            servicio.save()
            messages.success(request, 'Servicio registrado')
            return redirect('/mantenedor_servicios')
        
    return render(request, 'registrarServicio.html') 

    # cod_servicio = form_reg_servicio.cod_servicio
    # nom_servicio = form_reg_servicio.nom_servicio
    # valor_unit = form_reg_servicio.valor_unit

    # valor_unit = float(valor_unit_str.replace(',', ''))

    # servicios = Servicio.objects.create(cod_servicio=cod_servicio, nom_servicio=nom_servicio, valor_unit=valor_unit)

@login_required
def edicionServicio(request, cod_servicio):
    servicios = Servicio.objects.get(cod_servicio=cod_servicio)
    context = {
        'servicios':servicios
    }
    return render(request, 'edicionServicio.html', context)

@login_required
def editarServicio(request):
    cod_servicio = request.POST.get('cod_servicio')
    nom_servicio = request.POST.get('nom_servicio')
    valor_unit_str = request.POST.get('valor_unit')

    valor_unit = float(valor_unit_str.replace(',', ''))

    servicios_get = Servicio.objects.get(cod_servicio=cod_servicio)

    servicios_get.nom_rec = nom_servicio
    servicios_get.valor_unit = valor_unit

    servicios_get.save()
    return redirect('/mantenedor_servicios')

@login_required
def eliminarServicio(request, cod_servicio):
    servicios = Servicio.objects.get(cod_servicio=cod_servicio)
    servicios.delete()

    return redirect('/mantenedor_servicios')

## Mantenedor Licencias ##
@login_required
def mantenedorLicencias(request):
    licencias = Licencia.objects.all()
    context = {
        'licencias':licencias
    }
    return render(request, 'mantenedor_licencias.html', context)

@login_required
def registrarLicencia(request):

    form_reg_licencia = LicenciaForm()

    if request.method == 'POST':
        form_reg_licencia = LicenciaForm(request.POST)
        if form_reg_licencia.is_valid():
            form_reg_licencia.save()
            messages.success(request, 'Licencia registrada')
            return redirect('/mantenedor_licencias')
        
    return render(request, 'registrarLicencia.html') 

@login_required
def edicionLicencia(request, cod_lic):
    licencias = Licencia.objects.get(cod_lic=cod_lic)
    context = {
        'licencias':licencias
    }
    return render(request, 'edicionLicencia.html', context)

@login_required
def editarLicencia(request):
    cod_lic = request.POST.get('cod_lic')
    nom_lic = request.POST.get('nom_lic')
    tipo_lic = request.POST.get('tipo_lic')
    costo_uf = request.POST.get('costo_uf')

    licencias_get = Licencia.objects.get(cod_lic=cod_lic)

    licencias_get.nom_lic = nom_lic
    licencias_get.tipo_lic = tipo_lic
    licencias_get.costo_uf = costo_uf

    licencias_get.save()
    return redirect('/mantenedor_licencias')

@login_required
def eliminarLicencia(request, cod_lic):
    licencias = Licencia.objects.get(cod_lic=cod_lic)
    licencias.delete()

    return redirect('/mantenedor_licencias')

    ##################################
## Getters de obtención de resultados ##
    ##################################
def getResultCpu(request):
    resultado_cpu = 0
    form = servidor_has_recurso_editForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            #Obtiene el valor de la tupla: 1,2,3,4,5,etc.
            cpu_choice = int(form.cleaned_data['cpu_choice'])
            #Por cada valor y label de la tupla dentro de la misma tupla ddValues la recorremos
            for cod_value, label in cpuValues:
                #Si el valor es igual al valor elegido en el select html entonces
                if cod_value == cpu_choice:
                    #asignamos el label a dd_label y rompemos el ciclo
                    cpu_label = label
                    break
            #logs propios para saber funcionamiento
            logging.info(cpu_choice)
            logging.info(cpu_label)

            # Recupera la cantidad específica de la base de datos
            # nom_rec_get = Recurso.objects.filter('nom_rec')
            recurso = Recurso.objects.get(nom_rec='Procesador')  # Aquí debes seleccionar el recurso correcto según tus necesidades
            logging.info(recurso)
            #Validamos que recurso sea el mismo objeto recurso y asi poder entrar en sus caracteristicas
            if recurso == recurso:
                logging.info(recurso)
                cantidad_especifica = recurso.valor_unit
                # Convierte dd_choice en un número (puedes usar int o float según tus necesidades)
                cpu_choice_numero = int(cpu_label)  #dd_label queda asignado como la etiqueta de la tupla
                logging.info(f'Cantidad específica: {cantidad_especifica}')
                logging.info(f'dd_choice_numero: {cpu_choice_numero}')
                # Realiza la multiplicación
                resultado_cpu = cpu_choice_numero * cantidad_especifica
                logging.info(f'Resultado de la multiplicación: {resultado_cpu}')
                # Haz lo que necesites con el resultado, por ejemplo, guardar en la base de datos o mostrarlo en la respuesta
    return round(resultado_cpu, 3)

def getResultRam(request):
    resultado_ram = 0
    form = servidor_has_recurso_editForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            #Obtiene el valor de la tupla: 1,2,3,4,5,etc.
            ram_choice = int(form.cleaned_data['ram_choice'])
            #Por cada valor y label de la tupla dentro de la misma tupla ddValues la recorremos
            for cod_value, label in ramValues:
                #Si el valor es igual al valor elegido en el select html entonces
                if cod_value == ram_choice:
                    #asignamos el label a dd_label y rompemos el ciclo
                    ram_label = label
                    break
            #logs propios para saber funcionamiento
            logging.info(ram_choice)
            logging.info(ram_label)

            # Recupera la cantidad específica de la base de datos
            recurso = Recurso.objects.get(nom_rec='Memoria RAM')  # Aquí debes seleccionar el recurso correcto según tus necesidades
            logging.info(recurso)

            #Validamos qMemoria RAM recurso sea el mismo objeto recurso y asi poder entrar en sus caracteristicas
            if recurso == recurso:
                logging.info(recurso)

                cantidad_especifica = recurso.valor_unit

                # Convierte dd_choice en un número (puedes usar int o float según tus necesidades)
                ram_choice_numero = int(ram_label)  #dd_label queda asignado como la etiqueta de la tupla

                logging.info(f'Cantidad específica: {cantidad_especifica}')
                logging.info(f'dd_choice_numero: {ram_choice_numero}')

                # Realiza la multiplicación
                resultado_ram = ram_choice_numero * cantidad_especifica
                logging.info(f'Resultado de la multiplicación: {resultado_ram}')

            # Haz lo que necesites con el resultado, por ejemplo, guardar en la base de datos o mostrarlo en la respuesta
    return round(resultado_ram, 3)

def getResultDD(request):
    resultado_dd = 0
    form = servidor_has_recurso_editForm(request.POST)
    if request.method == 'POST':
        if form.is_valid():
            #Obtiene el valor de la tupla: 1,2,3,4,5,etc.
            dd_choice = int(form.cleaned_data['dd_choice'])
            #Por cada valor y label de la tupla dentro de la misma tupla ddValues la recorremos
            for cod_value, label in ddValues:
                #Si el valor es igual al valor elegido en el select html entonces
                if cod_value == dd_choice:
                    #asignamos el label a dd_label y rompemos el ciclo
                    dd_label = label
                    break
            #logs propios para saber funcionamiento
            logging.info(dd_choice)
            logging.info(dd_label)

            # Recupera la cantidad específica de la base de datos
            recurso = Recurso.objects.get(nom_rec='Disco Duro')  # Aquí debes seleccionar el recurso correcto según tus necesidades
            logging.info(recurso)

            #Validamos que recurso sea el mismo objeto recurso y asi poder entrar en sus caracteristicas
            if recurso == recurso:
                logging.info(recurso)

                cantidad_especifica = recurso.valor_unit

                # Convierte dd_choice en un número (puedes usar int o float según tus necesidades)
                dd_choice_numero = int(dd_label)  #dd_label queda asignado como la etiqueta de la tupla

                logging.info(f'Cantidad específica: {cantidad_especifica}')
                logging.info(f'dd_choice_numero: {dd_choice_numero}')

                # Realiza la multiplicación
                resultado_dd = dd_choice_numero * cantidad_especifica
                logging.info(f'Resultado de la multiplicación: {resultado_dd}')

            # Haz lo que necesites con el resultado, por ejemplo, guardar en la base de datos o mostrarlo en la respuesta
    return round(resultado_dd, 3)

def getSumMonto(request):
    dd_label = 0
    cpu_label = 0
    ram_label = 0
    suma = 0
    montoCpu = getResultCpu(request)
    montoRam = getResultRam(request)
    montoDd = getResultDD(request)
    suma = round(montoCpu + montoRam + montoDd, 3)
    return suma

def getSumMonto_CLP(request):
    dd_label = 0
    cpu_label = 0
    ram_label = 0
    # uf_value = 36000
    # uf_value = UFValue.objects.get(id=1).value
    # uf_value = UFValueForm(request.POST) 
    cant_serv = int(request.POST.get('cant_serv', 1))
    uf_value = int(request.POST.get('value', 0))
    # UF = 36000
    suma = 0
    montoCpu = getResultCpu(request)
    montoRam = getResultRam(request)
    montoDd = getResultDD(request)
    montoSVC = getSumServicios(request)
    valor_SVC = int(montoSVC)
    suma = montoCpu + montoRam + montoDd
    total = int((suma * uf_value))
    total_con_svc = int((total + valor_SVC)*cant_serv)
    return total_con_svc

# def getSumServicios(request):
#     list_servicios = Servicio.objects.all()
#     boxes = request.POST.getlist('boxes')
#     boxes_int = [int(box) for box in boxes]
#     servicios_dict = {servicio.cod_servicio: servicio.valor_unit for servicio in list_servicios}
#     servicios_dict_nombres = {servicio.cod_servicio: servicio.nom_servicio for servicio in list_servicios}
#     valores = []
#     monto = 0
#     suma = 0.0

#     # porcentaje_usuario = float(request.POST.get('porcentaje', 'porcentaje'))
#     list_servicios.update(estado=False)
#     for box in boxes_int:
#         valor = int(servicios_dict.get(box, 'Valor no encontrado'))
#         nombre = servicios_dict_nombres.get(box, 'Nombre no encontrado')

#         # valor_con_porcentaje = valor * (1 + porcentaje_usuario / 100.0)
#         valores.append((nombre, valor))

#     for val in valores:
#         valor = val[1]
#         suma += valor

    
#     return suma

def getSumServicios(request):
    list_servicios = Servicio.objects.all()
    boxes = request.POST.getlist('boxes')
    boxes_int = [int(box) for box in boxes]
    servicios_dict = {servicio.cod_servicio: servicio.valor_unit for servicio in list_servicios}
    servicios_dict_nombres = {servicio.cod_servicio: servicio.nom_servicio for servicio in list_servicios}
    valores = []
    suma = 0.0

    # Obtén el porcentaje del formulario
    porcentaje = request.POST.get('porcentaje')
    list_servicios.update(porcentaje=porcentaje)
    if porcentaje is not None:
        try:
            porcentaje = float(porcentaje)
        except ValueError:
            porcentaje = 0.0  # En caso de entrada no válida

    list_servicios.update(estado=False)
    for box in boxes_int:
        valor_unit = servicios_dict.get(box, 0)  # Valor por defecto es 0 si no se encuentra
        nombre = servicios_dict_nombres.get(box, 'Nombre no encontrado')

        # Aplica el porcentaje si se proporcionó uno válido
        valor_unit1 = valor_unit * (1 - (porcentaje / 100))

        valores.append((nombre, valor_unit1))
        print('Este out corresponde a valores.append: ' + str(valores))

    for val in valores:
        valor = val[1]
        suma += valor

    return suma

## Mantenedores de ddValues, cpuValues y ramValues
@login_required
def mantenedorValues(request):
    ddValues = DdValues.objects.all()
    ramValues = RamValues.objects.all()
    cpuValues = CpuValues.objects.all()

    context = {
        'ddValues':ddValues,
        'ramValues':ramValues,
        'cpuValues':cpuValues,
    }
    return render(request, 'mantenedor_values.html', context)

########################### Mantendor ddValues ###########################
@login_required
def registrarDdValue(request):

    form_reg_ddValues = ddValuesForm()

    if request.method == 'POST':
        form_reg_ddValues = ddValuesForm(request.POST)
        if form_reg_ddValues.is_valid():
            form_reg_ddValues.save()
            messages.success(request, 'Valor registrado')
            return redirect('/mantenedor_values')
        
    return render(request, 'registrarDdValue.html') 

@login_required
def edicionDdValue(request, cod_value):
    ddValues = DdValues.objects.get(cod_value=cod_value)
    context = {
        'ddValues':ddValues
    }
    return render(request, 'edicionDdValue.html', context)

@login_required
def editarDdValue(request):
    cod_value = request.POST.get('cod_value')
    nom_value = request.POST.get('nom_value')

    ddValues_get = DdValues.objects.get(cod_value=cod_value)

    ddValues_get.cod_value = cod_value
    ddValues_get.nom_value = nom_value

    ddValues_get.save()
    return redirect('/mantenedor_values')

@login_required
def eliminarDdValue(request, cod_value):
    ddValues = DdValues.objects.get(cod_value=cod_value)
    ddValues.delete()

    return redirect('/mantenedor_values')

########################### Mantendor ramValues ###########################

@login_required
def registrarRamValue(request):

    form_reg_RamValues = ramValuesForm()

    if request.method == 'POST':
        form_reg_RamValues = ramValuesForm(request.POST)
        if form_reg_RamValues.is_valid():
            form_reg_RamValues.save()
            messages.success(request, 'Valor registrado')
            return redirect('/mantenedor_values')
        
    return render(request, 'registrarRamValue.html') 

@login_required
def edicionRamValue(request, cod_value):
    ramValues = RamValues.objects.get(cod_value=cod_value)
    context = {
        'ramValues':ramValues
    }
    return render(request, 'edicionRamValue.html', context)

@login_required
def editarRamValue(request):
    cod_value = request.POST.get('cod_value')
    nom_value = request.POST.get('nom_value')

    ramValues_get = RamValues.objects.get(cod_value=cod_value)

    ramValues_get.cod_value = cod_value
    ramValues_get.nom_value = nom_value

    ramValues_get.save()
    return redirect('/mantenedor_values')

@login_required
def eliminarRamValue(request, cod_value):
    ramValues = RamValues.objects.get(cod_value=cod_value)
    ramValues.delete()

    return redirect('/mantenedor_values')

########################### Mantendor cpuValues ###########################
@login_required
def registrarCpuValue(request):

    form_reg_CpuValues = CpuValuesForm()

    if request.method == 'POST':
        form_reg_CpuValues = CpuValuesForm(request.POST)
        if form_reg_CpuValues.is_valid():
            form_reg_CpuValues.save()
            messages.success(request, 'Valor registrado')
            return redirect('/mantenedor_values')
        
    return render(request, 'registrarCpuValue.html') 

@login_required
def edicionCpuValue(request, cod_value):
    cpuValues = CpuValues.objects.get(cod_value=cod_value)
    context = {
        'cpuValues':cpuValues
    }
    return render(request, 'edicionCpuValue.html', context)

@login_required
def editarCpuValue(request):
    cod_value = request.POST.get('cod_value')
    nom_value = request.POST.get('nom_value')

    cpuValues_get = CpuValues.objects.get(cod_value=cod_value)

    cpuValues_get.cod_value = cod_value
    cpuValues_get.nom_value = nom_value

    cpuValues_get.save()
    return redirect('/mantenedor_values')

@login_required
def eliminarCpuValue(request, cod_value):
    cpuValues = CpuValues.objects.get(cod_value=cod_value)
    cpuValues.delete()

    return redirect('/mantenedor_values')