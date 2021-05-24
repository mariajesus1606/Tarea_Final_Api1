#Programa que muestre los eventos internacionales según el artista (Palabra Clave) que introduzca el usuario.

#Importamos libreria requests
import requests

#Importamos la libreria json
import json

#Importar la libreria para que pueda leer nuestra key.
import os

#Guardaremos nuestra key en una variable de entorno.
key=os.environ["key"]

#importamos las fechas
from datetime import datetime 

#url base
url_base="https://app.ticketmaster.com/discovery/v2/"

def ev_artista (palabra_clave):
    #Creamos el diccionario con los parámetros necesarios
    payload = {'key':key,'keyword':palabra_clave}
    #Guardamos la petición en una variable(urlbase + diccionario con parametros)
    r=requests.get(url_base+'events',params=payload)
    #Inicializamos las listas necesarias
    nombres=[]
    fechas=[]
    horas=[]
    salas=[]
    direccion=[]
    ciudades=[]
    paises=[]
    urls=[]
    urls_sala=[]
    numelementos=0
    #Comprobamos que la peticion es correcta
    if r.status_code == 200:
        url_gestionada=r.url
        #Guardamos el contenido en json
        contenido = r.json()
        # Si la palabra clave no está en la variable guardada imprime un mensaje
        noms=[]
        for i in contenido["_embedded"]["events"]:
            noms.append(i["name"])
        for nombre in noms:
            if palabra_clave.upper() not in nombre.upper():
                mensaje=("No hay eventos para esa búsqueda")
                return mensaje
        else:
            #Para cada elemento en el contenido añadimos la informacion a las listas
            for elem in contenido["_embedded"]["events"]:
                #NOMBRES
                nombres.append(elem["name"])
                #CIUDADES
                ciudades.append(elem["_embedded"]["venues"][0]["city"]["name"])
                #PAISES
                paises.append(elem["_embedded"]["venues"][0]["country"]["name"])
                #SALAS
                salas.append(elem["_embedded"]["venues"][0]["name"])
                #DIRECCIONES
                if "address" in elem["_embedded"]["venues"][0]:
                    direccion.append(elem["_embedded"]["venues"][0]["address"]["line1"])
                else:
                    direccion.append("NO ESPECIFICADA")
                #FECHAS
                fechas.append(elem["dates"]["start"]["localDate"])
                #HORAS: A veces la hora no esta especificada así que nos aseguramos de ello.
                if "localTime" in elem["dates"]["start"]:
                    horas.append(elem["dates"]["start"]["localTime"])
                else:
                    horas.append("NO ESPECIFICADA")
                #URLS
                urls.append(elem["url"])
                urls_sala.append(elem["_embedded"]["venues"][0]["url"])
                if elem["_embedded"]["venues"][0]["url"]:
                    numelementos=numelementos+1
            filtro=[nombres,paises,ciudades,salas,direccion,fechas,horas,urls,urls_sala,numelementos]
        return filtro

artista=input("\nIntroduce el artista o palabra clave: ")
#Si lo que devuelve la funcion no es una lista imprime el mensaje.
if type(ev_artista(artista)) != list:
    print(ev_artista(artista))
    print("Programa terminado.")
    
#Si no, impime el contenido
else:
    #MOSTRAR CONTENIDO
    print("\nPara la búsqueda:",artista.upper(),"se han encontrado",ev_artista(artista)[9],"coincidencias.")
    for nombre,pais,ciudad,sala,direc,fecha,hora,url,urlsala in zip((ev_artista(artista)[0]),(ev_artista(artista)[1]),(ev_artista(artista)[2]),(ev_artista(artista)[3]),(ev_artista(artista)[4]),(ev_artista(artista)[5]),(ev_artista(artista)[6]),(ev_artista(artista)[7]),(ev_artista(artista)[8])):
        fecha_cambiada = datetime.strptime(fecha, '%Y-%m-%d')
        fecha_str = datetime.strftime(fecha_cambiada, '%d/%m/%Y')
        print("\n\nNOMBRE:",nombre,"\nPAIS:",pais,"\nCIUDAD:",ciudad,"\nSALA:",sala,"\nDIRECCION:",direc,"\nFECHA:",fecha_str,"\nHORA:",hora,"\nURL COMPRAR ENTRADA:",urlsala,"\n",url)
