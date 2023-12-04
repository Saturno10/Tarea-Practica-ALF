from entonar import entonar, clasificar_entonacion
from silabar import silabar
import csv
import ast

if __name__ == '__main__':
    diccionario = {}
    # Intentamos leer el archivo que contiene el diccionario de anteriores ejecuciones
    try:
        with open('diccionario.csv', 'r') as archivo:
            # Si lo encontramos, lo leemos
            lector = csv.reader(archivo)

            # Saltar la cabecera
            next(lector)

            # Leer cada fila del archivo
            for fila in lector:
                # por si había algún fallo en la escritura
                if len(fila) < 3:
                    break
                # Y añadimos al diccionario de esta ejecución todo lo que encontramos

                palabra = fila[0]
                silabas = ast.literal_eval(fila[1])  # Convertir la string a una lista
                entonacion = ast.literal_eval(fila[2])  # Convertir la string a una lista

                # Añadir la palabra al diccionario
                diccionario[palabra] = {"silabas": silabas, "entonación": entonacion}
            print("Diccionario encontrado, leyendo datos... \n")
        archivo.close()
    # Si no lo encontramos, creamos uno nuevo y le añadimos la cabecera
    except FileNotFoundError:
        with open('diccionario.csv', 'w', newline='') as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow(["Palabra", "Sílabas", "Entonación"])
            print("Diccionario no encontrado, construyendo diccionario vacío... \n")
        archivo.close()
    # Preparamos el archivo para escribirle lineas en caso de que añadan palabras nuevas
    with open('diccionario.csv', 'a', newline='') as archivo:

        escritor = csv.writer(archivo)
        # Seleccionamos modo
        entrada = None
        while entrada not in ("1", "2", "3", "4", "5"):
            print("---EJECUTANDO PROGRAMA DE PRÁCTICA DE AUTÓMATAS Y LENGUAJES FORMALES---\n1. Silabear una palabra.\n"
                  "2. Clasificar palabra según su entonación\n3. Obtener palabras que rimen con una palabra\n4. "
                  "Justificar texto\n5. Salir")

            entrada = str(input("Elige la opción que quieres escribiendo su número: "))
            match entrada:
                # Silabar
                case "1":
                    palabra = ""
                    while palabra != "0":
                        palabra = str(input("Introduce la palabra que quieres silabear, procura que esté bien escrita."
                                            " Pon un 0 para terminar: "))
                        if palabra != "0":
                            # Si no está en el diccionario, lo insertamos. Sino simplemente leemos el diccionario
                            if palabra not in diccionario:
                                print("Palabra no encontrada en diccionario, procesando e insertando...")
                                silabas = silabar(palabra)
                                entonadas = entonar(silabas)
                                diccionario[palabra] = {"silabas": silabas, "entonacion": entonadas}
                                escritor.writerow([palabra, silabas, entonadas])
                                print("La palabra ", palabra, " silabada es: ", silabas)
                            else:
                                print("La palabra ya está en el diccionario, leyendo resultado...")
                                print("La palabra ", palabra, " silabada es: ", diccionario[palabra]["silabas"])
                    break
                # Entonar
                case "2":
                    palabra = ""
                    while palabra != "0":
                        palabra = str(input(
                            "Introduce la palabra que quieres clasificar según su entonación,"
                            " procura que esté bien escrita. Pon un 0 para terminar: "))
                        if palabra != "0":
                            # Si no está en el diccionario, lo insertarmos. Sino simpplemente leemos el diccionario
                            if palabra not in diccionario:
                                print("Palabra no encontrada en diccionario, procesando e insertando...")
                                silabas = silabar(palabra)
                                entonadas = entonar(silabas)
                                diccionario[palabra] = {"silabas": silabas, "entonacion": entonadas}
                                escritor.writerow([palabra, silabas, entonadas])
                                print("La palabra ", palabra, " entonada es: ", entonadas, "por lo que es:",
                                      clasificar_entonacion(entonadas), "\n")
                            else:
                                print("La palabra ya está en el diccionario, leyendo resultado...")
                                print("La palabra ", palabra, " entonada es: ", diccionario[palabra]["entonacion"],
                                      "por lo que es:", clasificar_entonacion(diccionario[palabra]["entonacion"]), "\n")
                    break
                # Rimas
                case "3":
                    print("No implementado")
                    break
                # Justificar
                case "4":
                    print("No implementado")
                    break
                # Salir
                case "5":
                    print("Iniciando fin de programa")
                    break
                case _:
                    print("Por favor, inserta un valor entre 1 y 3")
            archivo.write('\n')
    archivo.close()
    print("Saliendo del programa...")
