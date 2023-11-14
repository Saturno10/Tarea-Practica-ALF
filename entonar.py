import regex
from unidecode import unidecode



def entonar_con_tilde(silabas):
    silabas_nuevas = []
    for silaba in silabas:
        silaba_nueva = ""
        for letra in silaba:
            if letra in ("á","é","í","ó","ú"):
                silaba_nueva += unidecode(letra).upper()
            else:
                silaba_nueva+=letra
        silabas_nuevas.append(silaba_nueva)
    return silabas_nuevas

def entonar_sin_tilde(silaba):
    vocales=0
    nueva_silaba=""
    for letra in silaba:
        if letra in "aeiou":
            vocales+=1
    if vocales == 3:
        central = False
        for letra in silaba:
            if letra in "aeiou" and not central:
                central = True
                nueva_silaba+=letra
            elif letra in "aeiou" and central:
                nueva_silaba+= letra.upper()

    elif vocales == 2:
        segunda = False
        for letra in silaba:
            if letra in "aeo":
                nueva_silaba+= letra.upper()

            elif letra in "iu":
                if segunda:
                    nueva_silaba+= letra.upper()
                else:
                    segunda = True
                    nueva_silaba += letra
            else:
                nueva_silaba+=letra
    else:

        for letra in silaba:
            if letra in "aeiou":
                nueva_silaba += letra.upper()
            else:
                nueva_silaba += letra
    return nueva_silaba



def entonar(match,silabas):
    nuevas_silabas = []
    if match.group('R1'):
        nuevas_silabas = entonar_con_tilde(silabas)
    elif match.group('R2'):
        nuevas_silabas = silabas
        nuevas_silabas[-2] = entonar_sin_tilde(silabas[-2])
    elif match.group('R3'):
        nuevas_silabas = silabas
        nuevas_silabas[-3] = entonar_sin_tilde(silabas[-3])
        #return match.group('R3').upper()
    return nuevas_silabas


if __name__ == '__main__':

    # Cadena original y sus sílabas
    silabas = ["a","güe","ro"]
    cadena = "".join(silabas)

    # Expresión regular
    patron_entonacion_silabas= r'(?P<R1>[áéíóú])|(?P<R2>[snaeiou]$)|(?P<R3>[qwrtypdfghjklñzxcvbm]$)'

    match = regex.search(patron_entonacion_silabas, cadena)

    # Aplicar la función a la cadena
    nueva_cadena = "".join(entonar(match,silabas))

    print(nueva_cadena)
