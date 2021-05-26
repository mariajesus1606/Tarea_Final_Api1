#Programa en python que muestra los eventos internacionales según la palabra clave (artista) que introduzca el usuario. 

#Importamos la librería requests
import requests
#Importamos la libreria json
import json
#Importamos la librería os que va leer nuestra variable de entorno
import os

#Importamos las fechas
from datetime import datetime

#Guardamos la url base
url_base="https://app.ticketmaster.com/discovery/v2/"

#Guardamos nuestra key 
key=os.environ["apikey"]

#Función que recibe el nombre del artista y devuelve todos los eventos proximos del mismo
def ev_artista (palabra_clave):
    #Creamos el diccionario con los parámetros necesarios
    payload = {'apikey':key,'keyword':palabra_clave}
    #Guardamos la petición en una variable(urlbase + diccionario con parametros)
    r=requests.get(url_base+'events',params=payload)
    #Inicializamos las listas que vamos a usar
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
        contenido = r.json()
        #Si la palabra clave no está en la variable guardada imprime un mensaje
        noms=[]
        for i in contenido["_embedded"]["events"]:
            noms.append(i["name"])
        for nombre in noms:
            if palabra_clave.upper() not in nombre.upper():
                mensaje=("Lo siento!! No hay eventos para esa búsqueda")
                return mensaje
        else:
            #Para cada elemento en el contenido añadimos la informacion a las listas
            for elem in contenido["_embedded"]["events"]:
                #Guardamos los nombres
                nombres.append(elem["name"])
                #Guardamos las ciudades
                ciudades.append(elem["_embedded"]["venues"][0]["city"]["name"])
                #Guardamos los paises
                paises.append(elem["_embedded"]["venues"][0]["country"]["name"])
                #GUardamos las salas
                salas.append(elem["_embedded"]["venues"][0]["name"])
                #Guardamos las direcciones y si no esta especificada
                if "address" in elem["_embedded"]["venues"][0]:
                    direccion.append(elem["_embedded"]["venues"][0]["address"]["line1"])
                else:
                    direccion.append("NO ESPECIFICADA")
                #Guardamos las fechas
                fechas.append(elem["dates"]["start"]["localDate"])
                #Guardamos las horas y comprobamos si tiene la hora ya que algunos no la tienen
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
#Si lo que devuelve la funcion no es una lista imprime el mensaje, sino es asi, imprime el contenido
if type(ev_artista(artista)) != list:
    print(ev_artista(artista))
    print("Programa terminado.")
else:
    print("\nPara la búsqueda:",artista.upper(),"se han encontrado",ev_artista(artista)[9],"coincidencias.")
    for nombre,pais,ciudad,sala,direc,fecha,hora,url,urlsala in zip((ev_artista(artista)[0]),(ev_artista(artista)[1]),(ev_artista(artista)[2]),(ev_artista(artista)[3]),(ev_artista(artista)[4]),(ev_artista(artista)[5]),(ev_artista(artista)[6]),(ev_artista(artista)[7]),(ev_artista(artista)[8])):
        fecha_cambiada = datetime.strptime(fecha, '%Y-%m-%d')
        fecha_str = datetime.strftime(fecha_cambiada, '%d/%m/%Y')
        print("\n\nNOMBRE:",nombre,"\nPAIS:",pais,"\nCIUDAD:",ciudad,"\nSALA:",sala,"\nDIRECCION:",direc,"\nFECHA:",fecha_str,"\nHORA:",hora,"\nURL COMPRAR ENTRADA:",urlsala,"\n",url)
