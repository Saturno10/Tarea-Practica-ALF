from entonar import entonar, clasificar_entonacion
from silabar import silabar
from rimar import rimar_consonante, rimar_asonante
import csv
import ast

if __name__ == '__main__':
    # Vamos a usar un diccionario, donde está lo mínimo de este trabajo, para las rimas, se hará referencia a lo que hay
    # En él para mirar los otros ficheros
    diccionarioPalabras = {}

    # Intentamos leer los archivos donde tenemos todos los datos
    try:
        # Tratamos el diccionario de palabras, el diccionario base
        with open('diccionarioPalabras.csv', 'r') as archivoPalabras:
            # Si lo encontramos, lo leemos
            lectorPalabras = csv.reader(archivoPalabras)

            # Saltamos la cabecera, solo está para la comprensión del usuario
            next(lectorPalabras)

            # Leer cada fila tras la cabecera del archivoPalabras
            for fila in lectorPalabras:
                # por si había algún fallo en la escritura y porque el diccionario termina con una línea vacía
                if len(fila) < 3:
                    break
                # Añadimos a la variable diccionario de esta ejecución todo lo que encontramos

                palabra = fila[0]
                # Convertimos las string a listas para poder trabajar con ellas cómodamente
                silabas = ast.literal_eval(fila[1])
                entonacion = ast.literal_eval(fila[2])

                # Añadimos la palabra al diccionario
                diccionarioPalabras[palabra] = {"silabas": silabas, "entonacion": entonacion}
            print("Diccionario encontrado, leyendo datos... \n")
        archivoPalabras.close()
        # Para comprobar que están los otros tres ficheros, ya que si falta solo uno de los el apartado 3 dará fallo
        archivoAsonantes = open('diccionarioAsonantes.csv', 'r')
        archivoConsonantes = open('diccionarioConsonantes.csv', 'r')
        archivoAsonantes.close()
        archivoConsonantes.close()

    # Si no encontramos alguno de los ficheros, creamos nuevos ficheros vacíos (sobreescribiendo aquellos encontrados)
    except FileNotFoundError:
        with open('diccionarioPalabras.csv', 'w', newline='') as archivoPalabras:
            escritorPalabras = csv.writer(archivoPalabras)
            escritorPalabras.writerow(["Palabra", "Sílabas", "Entonación"])
        archivoPalabras.close()
        with open('diccionarioAsonantes.csv', 'w', newline='') as archivoAsonantes:
            escritorAsonantes = csv.writer(archivoAsonantes)
            escritorAsonantes.writerow(["Rima Asonante", "Palabras"])
        archivoAsonantes.close()
        with open('diccionarioConsonantes.csv', 'w', newline='') as archivoConsonantes:
            escritorConsonantes = csv.writer(archivoConsonantes)
            escritorConsonantes.writerow(["Rima Consonante", "Palabras"])
        archivoConsonantes.close()

        print("Diccionario no encontrado, construyendo diccionario vacío... \n")
    # Preparamos el archivoPalabras para poder actualizar el diccionario
    archivoPalabras = open('diccionarioPalabras.csv', 'a', newline='')

    escritorPalabras = csv.writer(archivoPalabras)

    # Seleccionamos modo de ejecución, solo se puede elegir un modo por ejecución, pero conserva todo lo que se ha hecho
    entrada = None
    while entrada not in ("1", "2", "3", "4", "5"):
        print("---EJECUTANDO PROGRAMA DE PRÁCTICA DE AUTÓMATAS Y LENGUAJES FORMALES---\n"
              "Selecciona el modo de esta ejecución:\n1. Silabear una palabra.\n"
              "2. Clasificar palabra según su entonación\n3. Obtener palabras que rimen con una palabra\n4. "
              "Justificar texto (NO IMPLEMENTADO. CIERRA EL PROGRAMA)\n5. Salir")

        entrada = str(input("Elige la opción que quieres escribiendo su número: "))
        match entrada:
            # Silabar
            case "1":
                palabra = ""
                while palabra != "0":
                    palabra = str(input("Introduce la palabra que quieres silabear, procura que esté bien escrita."
                                        " Pon un 0 para terminar: "))
                    if palabra != "0":
                        # Si no está en el diccionario, lo insertamos. Si está simplemente leemos el diccionario
                        if palabra not in diccionarioPalabras:
                            # Aprovechamos para insertar la palabra en todos los apartados
                            print("Palabra no encontrada en diccionario, procesando e insertando...")
                            silabas = silabar(palabra)
                            entonadas = entonar(silabas)
                            diccionarioPalabras[palabra] = {"silabas": silabas, "entonacion": entonadas}
                            rima_consonante = rimar_consonante(entonadas)
                            rima_asonante = rimar_asonante(rima_consonante)
                            escritorPalabras.writerow([palabra, silabas, entonadas])

                            with open('diccionarioConsonantes.csv', 'r') as archivoConsonantes:
                                reader = csv.reader(archivoConsonantes)
                                datos = list(reader)

                            # Busca las rimas en los archivos
                            for fila_rimas in datos:
                                if fila_rimas[0] == rima_consonante:
                                    # Si la rima existe, añade la palabra al final de la lista
                                    fila_rimas.append(palabra)
                                    break
                            else:
                                # Si la rima no existe, crea una nueva fila y añadimos la rima y la palabra
                                datos.append([rima_consonante, palabra])

                            # Abre el archivo en modo escritura y escribe los datos sobreescribiendo
                            # (Única manera rápida que he visto de añadir palabras a una fila individual)
                            with open('diccionarioConsonantes.csv', 'w', newline='') as archivoConsonantes:
                                writer = csv.writer(archivoConsonantes)
                                writer.writerows(datos)
                            # El razonamiento es lo mismo para las rimas asonantes
                            with open('diccionarioAsonantes.csv', 'r') as archivoAsonantes:
                                reader = csv.reader(archivoAsonantes)
                                datos = list(reader)

                            for fila_rimas in datos:
                                if fila_rimas[0] == rima_asonante:
                                    fila_rimas.append(palabra)
                                    break
                            else:

                                datos.append([rima_asonante, palabra])

                            # Abre el archivo en modo escritura y escribe los datos
                            with open('diccionarioAsonantes.csv', 'w', newline='') as archivoAsonantes:
                                writer = csv.writer(archivoAsonantes)
                                writer.writerows(datos)
                            # Mostramos la palabra silabada
                            print("La palabra ", palabra, " silabada es: ", silabas)
                        else:
                            # Si ya la tenemos simplemente la leemos
                            print("La palabra ya está en el diccionario, leyendo resultado...")
                            print("La palabra ", palabra, " silabada es: ", diccionarioPalabras[palabra]["silabas"])
                break
            # Entonar
            case "2":
                palabra = ""
                while palabra != "0":
                    palabra = str(input(
                        "Introduce la palabra que quieres clasificar según su entonación,"
                        " procura que esté bien escrita. Pon un 0 para terminar: "))
                    if palabra != "0":
                        # Mismo razonamiento de inserción que con las sílabas
                        # Lo único que cambia es que en el diccionario buscamos la entoncación
                        if palabra not in diccionarioPalabras:
                            print("Palabra no encontrada en diccionario, procesando e insertando...")
                            silabas = silabar(palabra)
                            entonadas = entonar(silabas)
                            diccionarioPalabras[palabra] = {"silabas": silabas, "entonacion": entonadas}
                            escritorPalabras.writerow([palabra, silabas, entonadas])
                            print("La palabra ", palabra, " entonada es: ", entonadas, "por lo que es:",
                                  clasificar_entonacion(entonadas), "\n")

                            rima_consonante = rimar_consonante(entonadas)
                            rima_asonante = rimar_asonante(rima_consonante)
                            with open('diccionarioConsonantes.csv', 'r') as archivoConsonantes:
                                reader = csv.reader(archivoConsonantes)
                                datos = list(reader)

                            for fila_rimas in datos:
                                if fila_rimas[0] == rima_consonante:
                                    fila_rimas.append(palabra)
                                    break
                            else:

                                datos.append([rima_consonante, palabra])

                            with open('diccionarioConsonantes.csv', 'w', newline='') as archivoConsonantes:
                                writer = csv.writer(archivoConsonantes)
                                writer.writerows(datos)

                            with open('diccionarioAsonantes.csv', 'r') as archivoAsonantes:
                                reader = csv.reader(archivoAsonantes)
                                datos = list(reader)

                            for fila_rimas in datos:
                                if fila_rimas[0] == rima_asonante:
                                    fila_rimas.append(palabra)
                                    break
                            else:

                                datos.append([rima_asonante, palabra])

                            with open('diccionarioAsonantes.csv', 'w', newline='') as archivoAsonantes:
                                writer = csv.writer(archivoAsonantes)
                                writer.writerows(datos)
                        else:
                            print("La palabra ya está en el diccionario, leyendo resultado...")
                            print("La palabra ", palabra, " entonada es: ", diccionarioPalabras[palabra]["entonacion"],
                                  "por lo que es:", clasificar_entonacion(diccionarioPalabras[palabra]["entonacion"]),
                                  "\n")
                break
            # Rimas
            case "3":

                palabra = None
                while palabra != "0":
                    palabra = str(input("Introduce la palabra de la que quieres que saquemos rimas. Pon un 0"
                                        " para terminar: "))
                    if palabra != "0":
                        # Mismo razonamiento que para el resto de opciones, pero tenemos que buscar en los ficheros
                        # La rima y si la palabra está ya o no
                        if palabra not in diccionarioPalabras:
                            print("Palabra no encontrada en diccionario, procesando e insertando...")
                            silabas = silabar(palabra)
                            entonadas = entonar(silabas)
                            diccionarioPalabras[palabra] = {"silabas": silabas, "entonacion": entonadas}
                            escritorPalabras.writerow([palabra, silabas, entonadas])
                            rimaConsonante = rimar_consonante(entonadas)
                            rimaAsonante = rimar_asonante(rimaConsonante)
                            with open('diccionarioConsonantes.csv', 'r') as archivoConsonantes:
                                reader = csv.reader(archivoConsonantes)
                                datos = list(reader)

                            # Busca la rima en el archivo
                            for fila_rimas in datos:
                                if fila_rimas[0] == rimaConsonante:
                                    # Si la rima existe, añade la palabra al final de la lista
                                    fila_rimas.append(palabra)
                                    break
                            else:
                                # Si la rima no existe, crea una nueva fila y la añade a la lista
                                datos.append([rimaConsonante, palabra])

                            # Abre el archivo en modo escritura y escribe los datos, sobreescribiendo el archivo entero
                            with open('diccionarioConsonantes.csv', 'w', newline='') as archivoConsonantes:
                                writer = csv.writer(archivoConsonantes)
                                writer.writerows(datos)
                            # Mismo algoritmo para las rimas asonantes
                            with open('diccionarioAsonantes.csv', 'r') as archivoAsonantes:
                                reader = csv.reader(archivoAsonantes)
                                datos = list(reader)

                            i = 0
                            for fila_rimas in datos:

                                if fila_rimas[0] == rimaAsonante:
                                    fila_rimas.append(palabra)
                                    break
                                i += 1

                            else:

                                datos.append([rimaAsonante, palabra])

                            with open('diccionarioAsonantes.csv', 'w', newline='') as archivoAsonantes:
                                writer = csv.writer(archivoAsonantes)
                                writer.writerows(datos)
                            palabrasConsonantes = []
                            # Va a la posición de la rima y guarda todas las palabras que no sean la de la entrada
                            with open('diccionarioConsonantes.csv', 'r') as archivoConsonantes:
                                reader = csv.reader(archivoConsonantes)
                                next(reader)
                                datos = list(reader)
                                i = 0
                                for fila in datos:
                                    if fila[0] == rimaConsonante:
                                        break
                                    i += 1
                                for palabras in datos[i][1:]:
                                    if palabras != palabra:
                                        palabrasConsonantes.append(palabras)
                            archivoConsonantes.close()
                            palabrasAsonantes = []
                            rimaAsonante = rimar_asonante(rimaConsonante)
                            with open('diccionarioAsonantes.csv', 'r') as archivoAsonantes:
                                reader = csv.reader(archivoAsonantes)
                                next(reader)
                                datos = list(reader)
                                i = 0
                                for fila in datos:
                                    if fila[0] == rimaAsonante:
                                        break
                                    i += 1
                                for palabras in datos[i][1:]:
                                    if palabras != palabra:
                                        palabrasAsonantes.append(palabras)
                            archivoConsonantes.close()
                            # Imprime el resultado
                            print("Palabras que riman con", palabra + ":\n Rima consonante:", palabrasConsonantes,
                                  "\n Rima asonante:", palabrasAsonantes)
                        else:
                            # Como antes, busca la rima y se queda con las palabras que no son las de la entrada
                            print("La palabra ya está en el diccionario, leyendo resultado...")
                            palabrasConsonantes = []
                            palabrasAsonantes = []
                            rimaConsonante = rimar_consonante(diccionarioPalabras[palabra]["entonacion"])
                            with open('diccionarioConsonantes.csv', 'r') as archivoConsonantes:
                                reader = csv.reader(archivoConsonantes)
                                next(reader)
                                datos = list(reader)
                                i = 0
                                for fila in datos:
                                    if fila[0] == rimaConsonante:
                                        break
                                    i += 1
                                for palabras in datos[i][1:]:
                                    if palabras != palabra:
                                        palabrasConsonantes.append(palabras)
                            archivoConsonantes.close()

                            rimaAsonante = rimar_asonante(rimaConsonante)
                            with open('diccionarioAsonantes.csv', 'r') as archivoAsonantes:
                                reader = csv.reader(archivoAsonantes)
                                next(reader)
                                datos = list(reader)
                                i = 0
                                for fila in datos:
                                    if fila[0] == rimaAsonante:
                                        break
                                    i += 1
                                for palabras in datos[i][1:]:
                                    if palabras != palabra:
                                        palabrasAsonantes.append(palabras)
                            archivoConsonantes.close()
                            print("Palabras que riman con", palabra + ":\n Rima consonante:", palabrasConsonantes,
                                  "\n Rima asonante:", palabrasAsonantes)
                break

            # Justificar NO IMPLEMENTADO
            case "4":
                print("No implementado")
                break
            # Salir
            case "5":
                print("Iniciando fin de programa")
                break
            # Cualquier cosa que no sea lo que se pida pondrá activará el bucle de vuelta
            case _:
                print("Por favor, inserta un valor entre 1 y 5")
        archivoPalabras.write('\n')
    archivoPalabras.close()

    print("Saliendo del programa...")
