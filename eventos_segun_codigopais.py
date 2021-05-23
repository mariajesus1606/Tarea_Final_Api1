#Programa que muestre segun el código del pais todos los eventos, con el nombre del artista, la fecha, el lugar y la url para poder comprar las entradas.

#Importamos libreria requests
import requests

#Importamos la libreria json
import json

#Importar la libreria para que pueda leer nuestra key.
import os

#Guardaremos nuestra key en una variable de entorno.
key=os.environ["apikey"]

#importamos las fechas
from datetime import datetime 

#url base
url_base="https://app.ticketmaster.com/discovery/v2/"
