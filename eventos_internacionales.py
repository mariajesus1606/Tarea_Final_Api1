#Programa que muestre los eventos internacionales según el artista (Palabra Clave) que introduzca el usuario.

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
