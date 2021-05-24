#Programa que muestre segun el código del pais todos los eventos, con el nombre del artista, la fecha, el lugar y la url para poder comprar las entradas.

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

#Obtener el total de páginas:
payload = {'key':key}
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
    #Creamos el diccionario con los parámetros necesarios
    payload = {'key':key,'countryCode':codigo_pais,'page':numero_pagina}
    #Guardamos la petición en una variable(urlbase + diccionario con parametros)
    r=requests.get(url_base+'events',params=payload)
    #Inicializamos las listas necesarias
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
        #Guardamos el contenido en json
        contenido = r.json()
        # Si el total de elementos es igual a 0 devuelve un mensaje
        total_pag=contenido["page"].get("totalElements")
        if total_pag == 0:
            mensaje=("No hay eventos en el país indicado")
            return mensaje
        else:
            #Añadimos la información a cada lista
            for elem in contenido["_embedded"]["events"]:
                nombres.append(elem["name"])
                urls.append(elem["url"])
                fechas.append(elem["dates"]["start"]["localDate"])
                #A veces la hora no esta especificada así que nos aseguramos de ello.
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
#Mientras numero de pagina sea distinto de * hacemos todo el procedimiento
while num != 0:
    #Pedimos al usuario el código del país
    if codpais == "":
        codpais=input("\nIntroduce el código del pais: ")
    else:
        None
    #Guardamos los códigos recortados en una lista
    codigos=[]
    for i in codigos_paises:
        codigos.append(i[:2])

    #Validar codigo pais
    while codpais not in codigos:
        print("\n¡Error!")
        print("\n-> El Código del país no es correcto.")
        print("\n-> El Código se compone de dos caracteres en mayúsculas")
        respuesta=input("\n¿Quieres ver las lista de códigos disponible?"'(s/n): ')
        #Validar respuesta
        if 's' not in respuesta and 'n' not in respuesta:
            print("\nPorfavor introduce s o n para responder")
            respuesta=input("\n¿Quieres ver las lista de códigos disponible?"'(s/n): ')
        elif respuesta == 's':
            for elem in codigos_paises:
                print(elem)
            codpais=input("\nIntroduce el código del pais: ")
        else:
            codpais=input("\nIntroduce el código del pais: ")

    #MOSTRAR CONTENIDO
    #Si lo que devuelve la funcion no es una lista imprime el mensaje.
    if type(mostrar_evento(codpais,num)) != list: 
        print(mostrar_evento(codpais,num))
        print("Programa terminado.")
        break
    #Si no, impime el contenido
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
