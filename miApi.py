from http.client import HTTPException
from logging.config import dictConfig
from logging import Logger

from fastapi import FastAPI, HTTPException, status

print("Mensaje de inicio")

app = FastAPI()
print("API creada")

# GET MATRICULAS--------------------------------------------------------------------------------------------------------
@app.get("/matriculas")
async def root():
    try:
        with open("ultimasPosiciones.txt", "r") as archivo:
            listaDatos = []
            lineas = archivo.readlines()
            print("Archivo leído correctamente.")
            texto = ""

            for linea in lineas:
                try:
                    datos = linea.strip().split(' - ')

                    if len(datos) != 3:
                        continue

                    diccDatos = {
                        "matricula": datos[0],
                        "ubicacion": datos[1],
                        "fecha": datos[2]
                    }

                    listaDatos.append(diccDatos)

                except ValueError as e:
                    print(f"Error al procesar línea: {linea.strip()} - {str(e)}")

            return {"status": "success", "datos": listaDatos}

    except FileNotFoundError:
        raise HTTPException(status_code=500, detail="El archivo 'ultimasPosiciones.txt' no fue encontrado")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error inesperado: {str(e)}")

# GET UNA MATRICULA-----------------------------------------------------------------------------------------------------
@app.get("/matriculas/{matricula}")
async def buscar_matricula(matricula: str):
    try:
        print(f"Buscando la matrícula: {matricula}")
        with open("ultimasPosiciones.txt", "r") as archivo:

            lineas = archivo.readlines()
            print("Archivo leído correctamente.")

            texto = ""
            for linea in lineas:


                    datos = linea.strip().split(' - ')
                    if len(datos) != 3:
                        continue

                    if matricula == datos[0]:
                        return {
                            "status": "success",
                            "data": {
                                "matricula": datos[0],
                                "ubicacion": datos[1],
                                "fecha": datos[2]
                            }
                        }

    except FileNotFoundError:

        print("El archivo no se encuentra.")

        raise HTTPException(status_code=404, detail="Archivo no encontrado")

    except Exception as e:

        print(f"Error desconocido: {str(e)}")

        raise HTTPException(status_code=500, detail=f"Error interno: {str(e)}")

# AÑADIR MATRICULA------------------------------------------------------------------------------------------------------
@app.post("/matriculas")
async def agregar_matricula(matricula: str, latitud: str, longitud: str, fecha: str):

    try:
        with open("ultimasPosiciones.txt", "a") as archivo:

            archivo.write(f"{matricula} - ['{latitud}', '{longitud}'] - {fecha}")

        return {"status": "success", "message": "Matrícula añadida con éxito"}

    except Exception as e:

        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail=f"No se pudo agregar la matrícula: {str(e)}")

# ELIMINAR MATRICULA----------------------------------------------------------------------------------------------------
@app.delete("/matriculas/{matricula}")
async def eliminar_matricula(matricula:str):

    try:

        encontrado = False

        with open("ultimasPosiciones.txt", "r") as archivo:

            lineas = archivo.readlines()

        with open("ultimasPosiciones.txt", "w") as archivo:

            for linea in lineas:

                datos = linea.strip().split(' - ')

                if len(datos) != 3 or datos[0] != matricula:
                    archivo.write(linea)
                else:
                    encontrado = True


        if not encontrado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matrícula no encontrada")

        return {"status": "success", "message": "Matrícula eliminada"}

    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Archivo no encontrado")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"No se pudo eliminar la matrícula: {str(e)}")

# MODIFICAR FECHA/UBICACION DE MATRICULA--------------------------------------------------------------------------------
@app.put("/matriculas/{matricula}")
async def modificar_matricula(matricula:str, nueva_latitud: str, nueva_longitud: str, nueva_fecha: str):

    try:

        encontrado = False

        with open("ultimasPosiciones.txt", "r") as archivo:

            lineas = archivo.readlines()

        with open("ultimasPosiciones.txt", "w") as archivo:

            for linea in lineas:

                datos = linea.strip().split(' - ')

                if len(datos) == 3 or datos[0] == matricula:

                    archivo.write(f"{matricula} - ['{nueva_latitud}', '{nueva_longitud}'] - {nueva_fecha}")

                    encontrado = True

                else:

                    archivo.write(linea)

        if not encontrado:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Matrícula no encontrada")

        return {"status": "success", "message": "Matrícula modificada"}

    except FileNotFoundError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Archivo no encontrado")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"No se pudo eliminar la matrícula: {str(e)}")