#Programa que muestre segun las fechas indicadas, la sala, el lugar y los artistas que van a actuar proximamente en España.

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

#Ponemos el codigo en una variable 'ES'
code='ES'

#Guardamos en un diccionario nuestros payload(parametros)
payload = {'key':key,'countryCode':code}

#Guardamos en una variable 'r', una peticion en la cual añadimos los parametros
r=requests.get(url_base+'venues.json',params=payload)

#Función que recibe un identificador del lugar y devuelve el nombre del evento y la fecha en la que está previsto.

def mostrar_artista_fecha (id_lugar):
    parametros = {'key':key,'venueId':id_lugar}
    peticion=requests.get(url_base+'events',params=parametros)
    nombres=[]
    fechas=[]
    if peticion.status_code == 200:
        contenido = peticion.json()
        for elem in contenido["_embedded"]["events"]:
            nombres.append(elem["name"])
            fechas.append(elem["dates"]["start"]["localDate"])
        filtro=[nombres,fechas]
        return filtro


#Para asegurarnos que no hay errores consultamos el estado de la petición.
#Inicializamos las listas que nos hacen falta
salas=[]
lugares=[]
identificadores=[]
if r.status_code == 200:
    #Guardamos el contenido en una variable leido por json.
    doc = r.json()
    for lugar in doc["_embedded"]["venues"]:
        salas.append(lugar["name"])
        lugares.append(lugar["state"]["name"])
        identificadores.append(lugar["id"])
    filtro=[salas,lugares,identificadores]
    #Mostramos la sala y el lugar donde se encuentra. Segun el identificador del lugar muestra el nombre del artista y la fecha en la que actúa.
    for sala,lugar,ident in zip(filtro[0],filtro[1],filtro[2]):
        if mostrar_artista_fecha(ident):
            print()
            print("\nLUGAR: ",lugar,"\nSALA:",sala)
            print("\nArtistas que van a tocar en la sala proximamente:")
            for nom,fecha in zip((mostrar_artista_fecha(ident)[0]),(mostrar_artista_fecha(ident)[1])):
                fecha_cambiada = datetime.strptime(fecha, '%Y-%m-%d')
                fecha_str = datetime.strftime(fecha_cambiada, '%d/%m/%Y')
                print("- ",nom,"Fecha: ",fecha_str)   
