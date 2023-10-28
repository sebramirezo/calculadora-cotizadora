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

####################################################################
def index(request):
    # Obtener los resultados de las funciones
    resultado_dd = getResultDD(request)
    resultado_cpu = getResultCpu(request)
    resultado_ram = getResultRam(request)
    resultado_suma = getSumMonto(request)
    resultado_total = getSumMonto_CLP(request)
    resultados_dinamicos = getSumRecursosDinamicos(request)
    resultados_dinam_array = getResultRecursosDinamicos(request)
    
    # Obtener el recuento de los valores
    dd_values_count = DdValues.objects.count()
    ram_values_count = RamValues.objects.count()
    cpu_values_count = CpuValues.objects.count()

    #Actualiza valores del combo box
    ddValues = DdValues.objects.all()
    ramValues = RamValues.objects.all()
    cpuValues = CpuValues.objects.all()

    print(dd_values_count, ram_values_count, cpu_values_count)
    
    # Obtener la fecha actual
    fecha_actual = date.today()
    
    # Obtener objetos de la base de datos
    
    recursos = Recurso.objects.all()
    list_servicios = Servicio.objects.all()
    list_licencias = Licencia.objects.all()
    
    # Inicializar formularios
    form = servidor_has_recurso_editForm(request.POST if request.method == 'POST' else None)
    form_nom = ServidorForm(request.POST if request.method == 'POST' else None)
    form_servicios = ServicioForm(request.POST if request.method == 'POST' else None)
    form_licencias = LicenciaForm(request.POST if request.method == 'POST' else None)
    form_recursos = RecursoForm(request.POST if request.method == 'POST' else None)
    form_uf = UFValueForm(request.POST if request.method == 'POST' else None)
    
    # Inicializar variables
    uf_value = request.POST.get('value', 0)
    cant_serv = request.POST.get('cant_serv', 1)
    nom_serv = request.POST.get('nom_serv', 'Sin nombre aún')
    cantidades = {}
    valores_dinam = []
    # cantidad_rec = request.POST.get('cantidad', 0)
    for recurso in recursos:
        if recurso.cod_rec > 5:
            cantidad_rec = request.POST.get('cantidad'+str(recurso.cod_rec), 0)
            valor = int(cantidad_rec) * float(recurso.valor_unit)
            valores_dinam.append(valor)
            recursos.filter(pk=recurso.cod_rec).update(cantidad=cantidad_rec)
    
    recursos = Recurso.objects.all()
    
    if request.method == 'POST' and form.is_valid() and form_uf.is_valid():
        # Validar datos
        logging.info('Form validado')

        uf_value = form_uf.cleaned_data['value']
        
        
        for recurso in recursos:
            if recurso.cod_rec > 5:
                cantidad_rec = request.POST.get('cantidad'+str(recurso.cod_rec), 0)
                recursos.filter(pk=recurso.cod_rec).update(cantidad=cantidad_rec)

        # Obtener la etiqueta de dd_choice, cpu_choice y ram_choice
        dd_choice_label = form.instance.get_dd_choice_display()
        cpu_choice_label = form.instance.get_cpu_choice_display()
        ram_choice_label = form.instance.get_ram_choice_display()

        # Puedes usar estas etiquetas para almacenarlas en la base de datos
        form.instance.dd_choice = dd_choice_label
        form.instance.cpu_choice = cpu_choice_label
        form.instance.ram_choice = ram_choice_label
        form.save(commit=False)


        # Procesar las selecciones de servicios y licencias
        boxes = [int(box) for box in request.POST.getlist('boxes')]
        boxes_lic = [int(box) for box in request.POST.getlist('boxes_lic')]

        servicios_dict = {servicio.cod_servicio: servicio for servicio in list_servicios}
        licencias_dict = {licencia.cod_lic: licencia for licencia in list_licencias}
        list_servicios.update(estado=False)
        list_licencias.update(estado=False)

        valores = [(servicios_dict[box].nom_servicio, int(servicios_dict[box].valor_unit)) for box in boxes]
        valores_lic = [(licencias_dict[box].nom_lic, licencias_dict[box].costo_uf) for box in boxes_lic]

        list_servicios.filter(pk__in=boxes).update(estado=True)
        list_licencias.filter(pk__in=boxes_lic).update(estado=True)

        # Crear un contexto para pasar los datos a la plantilla
        context = {
            'form': form,
            'form_nom': form_nom,
            'nom_servidor': nom_serv,
            'cant_serv': cant_serv,
            'form_servicios': form_servicios,
            'form_licencias': form_licencias,
            'form_recursos':form_recursos,
            'form_uf': form_uf,
            'value': uf_value,
            'valor':valores_dinam,
            'fecha_actual': fecha_actual,
            'dd_choice_label': dd_choice_label,
            'cpu_choice_label': cpu_choice_label,
            'ram_choice_label': ram_choice_label,
            'resultado_dd': resultado_dd,
            'resultado_cpu': resultado_cpu,
            'resultado_ram': resultado_ram,
            'resultados_dinamicos':resultados_dinamicos,
            'resultados_dinam_array':resultados_dinam_array,
            'dd_values_count': dd_values_count,
            'ram_values_count': ram_values_count,
            'cpu_values_count': cpu_values_count,
            'suma': resultado_suma,
            'total': resultado_total,
            'list_servicios': list_servicios,
            'list_licencias': list_licencias,
            'list_recursos': recursos,
            'boxes': boxes,
            'boxes_lic': boxes_lic,
            'valores': valores,
            'valores_lic': valores_lic,
            'errors': form.errors.as_text()
        }
        return render(request, 'plantilla.html', context)
    
    # Crear un contexto para pasar los datos a la plantilla (GET request o formulario no válido)
    context = {
        'form': form,
        'form_nom': form_nom,
        'cant_serv': cant_serv,
        'form_uf': form_uf,
        'valor':valores_dinam,
        'value': uf_value,
        'list_recursos': recursos,
        'dd_values_count': dd_values_count,
        'ram_values_count': ram_values_count,
        'cpu_values_count': cpu_values_count,
        'form_servicios': form_servicios,
        'form_licencias': form_licencias,
        'form_recursos':form_recursos,
        'list_servicios': list_servicios,
        'list_licencias': list_licencias,
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
def registrarRecurso(request):

    form_reg_recurso = RecursoForm()

    if request.method == 'POST':
        form_reg_recurso = RecursoForm(request.POST)
        if form_reg_recurso.is_valid():

            max_cod = Recurso.objects.aggregate(models.Max('cod_rec'))['cod_rec__max']
            nuevo_cod = max_cod + 1

            recurso = form_reg_recurso.save(commit=False)
            recurso.cod = nuevo_cod
            recurso.save()
            messages.success(request, 'Recurso registrado')
            return redirect('/mantenedor_recursos')
        
    return render(request, 'registrarRecurso.html') 

@login_required
def edicionRecurso(request, cod_rec):
    recursos = Recurso.objects.get(cod_rec=cod_rec)
    recursosx = Recurso.objects.filter(cod_rec=cod_rec)

    context = {
        'recursos':recursos,
        'recursosx':recursosx
    }
    return render(request, 'edicionRecurso.html', context)

@login_required
def editarRecurso(request):
    cod_rec = request.POST.get('cod_rec')
    nom_rec = request.POST.get('nom_rec')
    valor_unit = request.POST.get('valor_unit')
    unidad = request.POST.get('unidad')

    recursos_get = Recurso.objects.get(cod_rec=cod_rec)

    recursos_get.nom_rec = nom_rec
    recursos_get.valor_unit = valor_unit
    recursos_get.unidad = unidad

    recursos_get.save()
    return redirect('/mantenedor_recursos')

@login_required
def eliminarRecurso(request, cod_rec):
    recursos = Recurso.objects.get(cod_rec=cod_rec)
    recursos.delete()

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


def get_result(request, resource_name, resource_id, resource_values):
    result = 0
    form = servidor_has_recurso_editForm(request.POST)

    if request.method == 'POST' and form.is_valid():
        resource_choice = int(form.cleaned_data[resource_name.lower() + '_choice'])

        for cod_value, label in resource_values:
            if cod_value == resource_choice:
                resource_label = label
                break

        logging.info(resource_choice)
        logging.info(resource_label)

        resource_obj = Recurso.objects.get(cod_rec=resource_id)  # Asegúrate de que el nombre del recurso coincida con el modelo de Recurso

        if resource_obj == resource_obj:
            logging.info(resource_obj)
            specific_amount = resource_obj.valor_unit
            resource_choice_number = int(resource_label)
            logging.info(f'Cantidad específica: {specific_amount}')
            logging.info(f'{resource_name}_choice_number: {resource_choice_number}')

            result = resource_choice_number * specific_amount
            logging.info(f'Resultado de la multiplicación: {result}')

    return round(result, 3)

def getResultCpu(request):
    resource_name = "CPU"
    resource_id = 1
    resource_values = cpuValues
    result = get_result(request, resource_name, resource_id, resource_values)
    return result

def getResultRam(request):
    resource_name = "RAM"
    resource_id = 3
    resource_values = ramValues
    result = get_result(request, resource_name, resource_id, resource_values)
    return result

def getResultDD(request):
    resource_name = "DD"
    resource_id = 5
    resource_values = ddValues
    result = get_result(request, resource_name, resource_id, resource_values)
    return result

def getResultRecursosDinamicos(request):
    recursos = Recurso.objects.all()
    total_array = []
    total = 0

    for recurso in recursos:
        if recurso.cod_rec > 5:
            cantidad = request.POST.get(f'cantidad{recurso.cod_rec}', 0)  # Obtén el valor de cantidad dinámicamente
            valor_unit = recurso.valor_unit
            total += int(cantidad) * valor_unit  # Realiza la multiplicación y suma al total

    return total

def getSumRecursosDinamicos(request):
    recursos = Recurso.objects.all()
    total = 0
    
    for recurso in recursos:
        cantidad = request.POST.get(f'cantidad{recurso.cod_rec}', 0)  # Obtén el valor de cantidad dinámicamente
        valor_unit = recurso.valor_unit
        total += int(cantidad) * valor_unit  # Realiza la multiplicación y suma al total

    return total

def getSumMonto(request):
    dd_label = 0
    cpu_label = 0
    ram_label = 0
    suma = 0
    montoRecDinamico = getSumRecursosDinamicos(request)
    montoCpu = getResultCpu(request)
    montoRam = getResultRam(request)
    montoDd = getResultDD(request)
    suma = round(montoCpu + montoRam + montoDd + montoRecDinamico, 3)
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
    montoRecDinamico = getSumRecursosDinamicos(request)
    montoSVC = getSumServicios(request)
    montoLic = getSumLicencia(request)
    valor_SVC = int(montoSVC)
    suma = montoCpu + montoRam + montoDd + montoRecDinamico
    total = int((suma * uf_value))
    total_con_svc = int((total + valor_SVC + montoLic)*cant_serv)
    return total_con_svc


def getSumServicios(request):
    list_servicios = Servicio.objects.all()
    boxes = request.POST.getlist('boxes')
    boxes_int = [int(box) for box in boxes]
    servicios_dict = {servicio.cod_servicio: servicio.valor_unit for servicio in list_servicios}
    servicios_dict_nombres = {servicio.cod_servicio: servicio.nom_servicio for servicio in list_servicios}
    valores = []
    suma = 0.0

    list_servicios.update(estado=False)
    for box in boxes_int:
        valor_unit = servicios_dict.get(box, 0)  # Valor por defecto es 0 si no se encuentra
        nombre = servicios_dict_nombres.get(box, 'Nombre no encontrado')

        valores.append((nombre, valor_unit))
        print('Este out corresponde a valores.append: ' + str(valores))

    for val in valores:
        valor = val[1]
        suma += valor

    return suma

def getSumLicencia(request):
    valores_lic = []
    suma = 0.0

    list_licencias = Licencia.objects.all()
    list_licencias.update(estado=False)

    boxes_lic = [int(box) for box in request.POST.getlist('boxes_lic')]
    licencias_dict = {licencia.cod_lic: licencia for licencia in list_licencias}
    valores_lic = [(licencias_dict[box].nom_lic, licencias_dict[box].costo_uf) for box in boxes_lic]

    for val in valores_lic:
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
            #Actualiza valores del combo box
            ddValues = DdValues.objects.all()
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
    label = request.POST.get('label')

    label = label.replace(',', '')

    ddValues_get = DdValues.objects.get(cod_value=cod_value)


    ddValues_get.cod_value = cod_value
    ddValues_get.label = label

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
            ramValues = RamValues.objects.all()
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
    label = request.POST.get('label')
    label = label.replace(',', '')

    ramValues_get = RamValues.objects.get(cod_value=cod_value)

    ramValues_get.cod_value = cod_value
    ramValues_get.label = label

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
            cpuValues = CpuValues.objects.all()
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
    label = request.POST.get('label')
    label = label.replace(',', '')

    cpuValues_get = CpuValues.objects.get(cod_value=cod_value)

    cpuValues_get.cod_value = cod_value
    cpuValues_get.label = label

    cpuValues_get.save()
    return redirect('/mantenedor_values')

@login_required
def eliminarCpuValue(request, cod_value):
    cpuValues = CpuValues.objects.get(cod_value=cod_value)
    cpuValues.delete()

    return redirect('/mantenedor_values')