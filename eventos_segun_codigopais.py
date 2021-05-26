#Programa que muestre segun el código del pais todos los eventos, con el nombre del artista, la fecha, el lugar y la url para poder comprar las entradas.

#Programa en python que muestra todos los eventos segun código del pais, con el artista o los artistas, la fecha, el lugar y la url para comprar la entrada

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


#Obtener el total de páginas:
payload = {'apikey':key}
p = requests.get(url_base+'events',params=payload)
if p.status_code == 200:
    doc = p.json()
    if doc["page"]:
        total_paginas=doc["page"].get("totalPages")

    
#Obtener la lista de codigos de paises, sacada de SUPPORTED COUNTRY CODES ("Esta lista la podemos leer en un fichero aparte si queremos")

codigos_paises=["US (United States Of America)",
"AD (Andorra)",
"AI (Anguilla)",
"AR (Argentina)",
"AU (Australia)",
"AT (Austria)",
"AZ (Azerbaijan)",
"BS (Bahamas)",
"BH (Bahrain)",
"BB (Barbados)",
"BE (Belgium)",
"BM (Bermuda)",
"BR (Brazil)",
"BG (Bulgaria)",
"CA (Canada)",
"CL (Chile)",
"CN (China)",
"CO (Colombia)",
"CR (Costa Rica)",
"HR (Croatia)",
"CY (Cyprus)",
"CZ (Czech Republic)",
"DK (Denmark)",
"DO (Dominican Republic)",
"EC (Ecuador)",
"EE (Estonia)",
"FO (Faroe Islands)",
"FI (Finland)",
"FR (France)",
"GE (Georgia)",
"DE (Germany)",
"GH (Ghana)",
"GI (Gibraltar)",
"GB (Great Britain)",
"GR (Greece)",
"HK (Hong Kong)",
"HU (Hungary)",
"IS (Iceland)",
"IN (India)",
"IE (Ireland)",
"IL (Israel)",
"IT (Italy)",
"JM (Jamaica)",
"JP (Japan)",
"KR (Korea, Republic of)",
"LV (Latvia)",
"LB (Lebanon)",
"LT (Lithuania)",
"LU (Luxembourg)",
"MY (Malaysia)",
"MT (Malta)",
"MX (Mexico)",
"MC (Monaco)",
"ME (Montenegro)",
"MA (Morocco)",
"NL (Netherlands)",
"AN (Netherlands Antilles)",
"NZ (New Zealand)",
"ND (Northern Ireland)",
"NO (Norway)",
"PE (Peru)",
"PL (Poland)",
"PT (Portugal)",
"RO (Romania)",
"RU (Russian Federation)",
"LC (Saint Lucia)",
"SA (Saudi Arabia)",
"RS (Serbia)",
"SG (Singapore)",
"SK (Slovakia)",
"SI (Slovenia)",
"ZA (South Africa)",
"ES (Spain)",
"SE (Sweden)",
"CH (Switzerland)",
"TW (Taiwan)",
"TH (Thailand)",
"TT (Trinidad and Tobago)",
"TR (Turkey)",
"UA (Ukraine)",
"AE (United Arab Emirates)",
"UY (Uruguay)",
"VE (Venezuela)"]


#Función que recibe el código del país y devuelve el nombre, la sala, la dirección, la fecha y la url
def mostrar_evento (codigo_pais,numero_pagina):
    payload = {'apikey':key,'countryCode':codigo_pais,'page':numero_pagina}
    r=requests.get(url_base+'events',params=payload)
    #Inicializamos las listas que vamos a usar
    nombres=[]
    fechas=[]
    horas=[]
    salas=[]
    direccion=[]
    ciudades=[]
    urls=[]
    #Comprobamos que la peticion es correcta
    if r.status_code == 200:
        url_gestionada=r.url
        contenido = r.json()
        #Si el total de elementos es igual a 0 devuelve un mensaje
        total_pag=contenido["page"].get("totalElements")
        if total_pag == 0:
            mensaje=("Lo siento!! No hay eventos en el país indicado")
            return mensaje
        else:
            #Añadimos la información a cada lista
            for elem in contenido["_embedded"]["events"]:
                nombres.append(elem["name"])
                urls.append(elem["url"])
                fechas.append(elem["dates"]["start"]["localDate"])
                #Comprobamos si esta la hora porque a veces no esta
                if "localTime" in elem["dates"]["start"]:
                    horas.append(elem["dates"]["start"]["localTime"])
                else:
                    horas.append("NO ESPECIFICADA")
                salas.append(elem["_embedded"]["venues"][0]["name"])
                if "address" in elem["_embedded"]["venues"][0]:
                    direccion.append(elem["_embedded"]["venues"][0]["address"]["line1"])
                else:
                    direccion.append("NO ESPECIFICADA")
                ciudades.append(elem["_embedded"]["venues"][0]["city"]["name"])
            filtro=[nombres,fechas,horas,salas,direccion,ciudades,urls]
            return filtro

#Inicializamos las variables codigo de pais vacío y numero por defecto en 1, para que sea la primera página del contenido
codpais=""
num=1

while num != 0:
    if codpais == "":
        codpais=input("\nIntroduce el código del pais: ")
    else:
        None
    #Guardamos los códigos recortados en una lista
    codigos=[]
    for i in codigos_paises:
        codigos.append(i[:2])

    #Validamos codigo pais
    while codpais not in codigos:
        print("\nError!!!Codigo del Pais Incorrecto.Intentalo de nuevo.")
        respuesta=input("\n¿Quieres ver las lista de códigos disponible?"'(s/n): ')
        #Validamos la respuesta
        if 's' not in respuesta and 'n' not in respuesta:
            print("\nPorfavor introduce s o n para responder")
            respuesta=input("\n¿Quieres ver las lista de códigos disponible?"'(s/n): ')
        elif respuesta == 's':
            for elem in codigos_paises:
                print(elem)
            codpais=input("\nIntroduce el código del pais: ")
        else:
            codpais=input("\nIntroduce el código del pais: ")

    #Si lo que devuelve la funcion no es una lista imprime el mensaje y sino, imprime el contenido.
    if type(mostrar_evento(codpais,num)) != list: 
        print(mostrar_evento(codpais,num))
        print("Programa terminado.")
        break
    else:
        for nombre,fecha,hora,sala,direc,ciudad,url in zip((mostrar_evento(codpais,num)[0]),(mostrar_evento(codpais,num)[1]),(mostrar_evento(codpais,num)[2]),(mostrar_evento(codpais,num)[3]),(mostrar_evento(codpais,num)[4]),(mostrar_evento(codpais,num)[5]),(mostrar_evento(codpais,num)[6])):
            fecha_cambiada = datetime.strptime(fecha, '%Y-%m-%d')
            fecha_str = datetime.strftime(fecha_cambiada, '%d/%m/%Y')
            print("\n\nNOMBRE:",nombre,"\nURL COMPRAR ENTRADA:",url,"\nFECHA:",fecha_str,"\nHORA:",hora,"\nSALA:",sala,"\nDIRECCIÓN:",direc,"\nCIUDAD:",ciudad)
    siguiente_pagina=input("¿Quieres ir a la siguiente página?(S/N)")
    #Si el usuario indica s, incrementamos el número de página en uno para pasar de página. Esta variable se le indica a la función para que incremente la página.
    if siguiente_pagina.upper() == 'S':
        num = num + 1
    else:
        print("Programa terminado.")
        break
