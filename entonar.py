import regex
from silabar import silabar
from unidecode import unidecode

patron_entonacion_silabas = r'(?P<R1>[áéíóú])|(?P<R2>[snaeiou]$)|(?P<R3>[qwrtypdfghjklñzxcvbm]$)'


def entonar_con_tilde(silabas):
    silabas_nuevas = []
    for silaba in silabas:
        silaba_nueva = ""
        for letra in silaba:
            if letra in ("á", "é", "í", "ó", "ú"):
                silaba_nueva += unidecode(letra).upper()
            else:
                silaba_nueva += letra
        silabas_nuevas.append(silaba_nueva)
    return silabas_nuevas


def entonar_sin_tilde(silaba):
    vocales = 0
    nueva_silaba = ""
    for letra in silaba:
        if letra in "aeiou":
            vocales += 1
    if vocales == 3:
        central = False
        for letra in silaba:
            if letra in "aeiou" and not central:
                central = True
                nueva_silaba += letra
            elif letra in "aeiou" and central:
                nueva_silaba += letra.upper()

    elif vocales == 2:
        segunda = False
        for letra in silaba:
            if letra in "aeo":
                nueva_silaba += letra.upper()

            elif letra in "iu":
                if segunda:
                    nueva_silaba += letra.upper()
                else:
                    segunda = True
                    nueva_silaba += letra
            else:
                nueva_silaba += letra
    else:

        for letra in silaba:
            if letra in "aeiou":
                nueva_silaba += letra.upper()
            else:
                nueva_silaba += letra
    return nueva_silaba


def entonar(silabas):
    # Hacemos copia para que no modifique la lista original, que la usamos en un diccionario.
    copia_silabas = silabas.copy()
    match = regex.search(patron_entonacion_silabas, "".join(copia_silabas))
    nuevas_silabas = []
    if match.group('R1'):
        nuevas_silabas = entonar_con_tilde(copia_silabas)
    elif match.group('R2'):
        nuevas_silabas = copia_silabas
        nuevas_silabas[-2] = entonar_sin_tilde(copia_silabas[-2])
    elif match.group('R3'):
        nuevas_silabas = copia_silabas
        nuevas_silabas[-1] = entonar_sin_tilde(copia_silabas[-1])
        # return match.group('R3').upper()
    return nuevas_silabas


def clasificar_entonacion(silabas):
    copia_silabas = silabas.copy()
    if copia_silabas[-1] != copia_silabas[-1].lower():
        return "aguda"
    elif copia_silabas[-2] != copia_silabas[-2].lower():
        return "llana"
    elif copia_silabas[-3] != copia_silabas[-3].lower():
        return "esdrújula"
    else:
        return "sobreesdrújula"


if __name__ == '__main__':

    entrada = None

    while entrada not in ("1", "2", "3"):
        print("---EJECUTANDO TEST DE FRAGMENTO DE ENTONACIÓN---\n1. Entonar palabras escritas por teclado.\n2. Entonar"
              "palabras del fichero vocabuario.txt\n3. Salir\n")

        entrada = str(input("Elige la opción que quieres escribiendo su número: "))
        match entrada:
            case "1":
                palabra = ""
                while palabra != "0":
                    palabra = str(input("Introduce la palabra que quieres entonar, procura que esté bien escrita."
                                        " Pon un 0 para terminar: "))
                    if palabra != "0":
                        print(entonar(silabar(palabra)), "es una palabra",
                              clasificar_entonacion(entonar(silabar(palabra))))
                break
            case "2":
                with open('vocabulario.txt', 'r', encoding='utf-8') as f:
                    # Leemos cada línea del archivo
                    for linea in f:
                        # Eliminamos los espacios y tabulaciones
                        linea = linea.replace(' ', '').replace('\t', '').replace('\n', '')
                        print(entonar(silabar(linea)), "es una palabra", clasificar_entonacion(entonar(silabar(linea))))
                f.close()
                break
            case "3":
                break
            case _:
                print("Por favor, inserta un valor entre 1 y 3")
