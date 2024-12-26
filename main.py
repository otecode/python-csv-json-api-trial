import csv
import json
import geopy.distance
import datetime
from fastapi import FastAPI

# Variables
datos = []
archivo = open('reto.csv')
archivoJson = open('nuevo.json', 'w')
archivoUltimasPosiciones = open("ultimasPosiciones.txt", "w")
coordenadasPorMatricula = {}
coordenadasConFechaPorMatricula = {}

# Iterar el csv
lector = csv.reader(archivo)

next(lector) # Para saltar la primera línea con los títulos de las columnas y no introducir sus strings en los datos
for linea in lector:

    coche = {
        "Matricula":linea[0],
        "Latitud" : linea[1],
        "Longitud" : linea[2],
        "Distance" : linea[3],
        "Pos_date" : linea[4]
    }
    datos.append(coche)
    # setDeMatriculas.add(linea[0]) # Contiene matriculas unicas, para conocer la cantidad

archivoJson.write(json.dumps(datos, indent=4))

archivoJson.close()
archivoJson = open('nuevo.json', 'r')
contenidoJson = json.load(archivoJson)

# EXTRACCIÓN DE DISTANCIAS POR COORDENADAS----------------------------------------------------------------------------------------------------------------------------------------------

coordenadasPorMatricula.clear()

for medicion in contenidoJson:

    matricula = medicion["Matricula"]
    latitud = medicion["Latitud"]
    longitud = medicion["Longitud"]
    pos_date = medicion["Pos_date"]
    fechaAConvertir = int(pos_date) / 1000
    fecha = datetime.datetime.utcfromtimestamp(fechaAConvertir).strftime('%d/%m/%Y %H:%M:%S')

    if (matricula not in coordenadasPorMatricula):
        coordenadasPorMatricula[matricula] = [[latitud, longitud, fecha]]

    else:
        coordenadasPorMatricula[matricula].append([latitud, longitud, fecha])

# RECORER CADA MATRÍCULA, Y DE CADA MATRÍCULA CALCULAR DISTANCIA DE UN PUNTO AL SIGUIENTE. ACUMULAR RESULTADOS EN UNA VARIABLE SUMATORIO

# Por cada matrícula
for matricula in coordenadasPorMatricula:

    # Muestro su matrícula, coordenadas leídas
    distanciaTotal = 0
    fechas = []
    print(f"Matricula: {matricula}")
    #print(f"Coordenadas leídas de la matrícula: {coordenadasPorMatricula[matricula]}")

    cantidadCoordenadas = len(coordenadasPorMatricula[matricula])

    # Recorro sus coordenadas

    for num in range(cantidadCoordenadas - 1):

        if (num >= 0):

            # Guardo una coordenada y la siguiente, la distancia entre ellas, y añado la distancia a la variable sumatorio.

            punto1 = [coordenadasPorMatricula[matricula][num][0], coordenadasPorMatricula[matricula][num][1]]
            punto2 = [coordenadasPorMatricula[matricula][num + 1][0], coordenadasPorMatricula[matricula][num + 1][1]]
            distanciaDelDesplazamiento = geopy.distance.geodesic(punto1, punto2).km
            distanciaTotal = distanciaTotal + distanciaDelDesplazamiento
            fechas.append(coordenadasPorMatricula[matricula][num][2])

            print("\nViaje de " + str(punto1) + " a " + str(punto2) + ". Distancia: " + str(distanciaDelDesplazamiento) + " - Fecha: " + coordenadasPorMatricula[matricula][num][2])

    # print(f"Distancia total recorrida por la matrícula: {distanciaTotal}")

    if (len(fechas) > 0):

        ultimaFecha = fechas[len(fechas)-1]

    # Tengo las fechas, fechas[0] será la última registrada

    for num in range(cantidadCoordenadas - 1):

        fecha = coordenadasPorMatricula[matricula][num][2]
        ubicacion = [coordenadasPorMatricula[matricula][num][0], coordenadasPorMatricula[matricula][num][1]]

        if (fecha == ultimaFecha):

            print(f"{matricula} - {ubicacion} - {fecha}")
            archivoUltimasPosiciones.write(f"{matricula} - {ubicacion} - {fecha}\n")


