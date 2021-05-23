#Programa que muestre segun las fechas indicadas, la sala, el lugar y los artistas que van a actuar proximamente en España.

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
