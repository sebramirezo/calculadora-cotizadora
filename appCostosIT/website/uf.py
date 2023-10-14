import requests
from .models import UFValue

def getValorUF_Api():
    # URL de la API
    url = "https://mindicador.cl/api/uf"

    # Realizar la solicitud GET a la API
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Analizar la respuesta JSON
        data = response.json()
        
        # Obtener el valor de la UF como un entero
        valor_uf = int(data['serie'][0]['valor'])

        UFValue.objects.update_or_create(id=1, defaults={"value": valor_uf})
        
        print("Valor de la UF:", valor_uf)
    else:
        print("Error al obtener los datos de la API")

    return valor_uf

def actualizarValorUF_Api():
    # URL de la API
    url = "https://mindicador.cl/api/uf"

    # Realizar la solicitud GET a la API
    response = requests.get(url)

    # Verificar si la solicitud fue exitosa
    if response.status_code == 200:
        # Analizar la respuesta JSON
        data = response.json()
        
        # Obtener el valor de la UF como un entero
        valor_uf = int(data['serie'][0]['valor'])

        UFValue.objects.update_or_create(id=1, defaults={"value": valor_uf})
        
        print("Valor de la UF:", valor_uf)
    else:
        print("Error al obtener los datos de la API")

    return valor_uf
