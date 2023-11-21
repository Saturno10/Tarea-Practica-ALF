import regex

#Expresión regular completa para silabar
patron_separacion_silabas = r'(?i)((?<R5b>((?P<s1_R5b1>[AEO])(?P<s2_R5b1>H?[ÚÍ]))|((?P<s1_R5b2>[ÚÍ])(?P<s2_R5b2>H?[AEO]))|((?P<s1_R5b3>[AÁ])(?P<s2_R5b3>H?[AÁ]))|((?P<s1_R5b4>[EÉ])(?P<s2_R5b4>H?[EÉ]))|((?P<s1_R5b5>[IÍ])(?P<s2_R5b5>H?[IÍ]))|((?P<s1_R5b6>[OÓ])(?P<s2_R5b6>H?[OÓ]))|((?P<s1_R5b7>[UÚ])(?P<s2_R5b7>H?[UÚ]))|((?P<s1_R5b8>[AEOÁÉÓ])(?P<s2_R5b8>H?[AEO]))|((?P<s1_R5b9>[AEO])(?P<s2_R5b9>H?[AEOÁÉÓ])))|' \
                 r'(?P<R1>(?P<s1_R1>[AEIOUÁÉÍÓÚÜ])(?P<s2_R1>(CH|LL|RR|[BCDFGJKLMNÑPQRSTVWXYZ])[AEIOUÁÉÍÓÚÜY]))|' \
                 r'(?P<R2a>(?P<s1_R2a>[AEIOUÁÉÍÓÚÜ])(?P<s2_R2a>([PCBGF])([RL])[AEIOUÁÉÍÓÚÜ]))|' \
                 r'(?P<R2b>(?P<s1_R2b>[AEIOUÁÉÍÓÚÜ])(?P<s2_R2b>([DT])([R])[AEIOUÁÉÍÓÚÜ]))|' \
                 r'(?P<R2c1>(?P<s1_R2c1>[AEIOUÁÉÍÓÚÜ][DHJKLMNÑQRSTVWXYZ])(?P<s2_R2c1>(LL|CH|[BCDFGHJKMNÑPQSTVWXYZ])[AEIOUÁÉÍÓÚÜ]))|' \
                 r'(?P<R2c2>(?P<s1_R2c2>[AEIOUÁÉÍÓÚÜ][BCFGHJKLMNÑPQRSVWXYZ])(?P<s2_R2c2>(LL|CH|[BCDFGHJKLMNÑPQSTVWXYZ])[AEIOUÁÉÍÓÚÜ]))|' \
                 r'(?P<R3a>(?P<s1_R3a>[AEIOUÁÉÍÓÚÜ][B-DF-HJ-NP-TV-ZÑ])(?P<s2_R3a>(([PCBGF][RL])|([DT][R]))[AEIOUÁÉÍÓÚÜ]))|' \
                 r'(?P<R3b>(?P<s1_R3b>[AEIOUÁÉÍÓÚÜ][BDNMLR]S)(?P<s2_R3b>[B-DF-HJ-ÑP-TV-Z][AEIOUÁÉÍÓÚÜ]))|' \
                 r'(?P<R3c>(?P<s1_R3c>[AEIOUÁÉÍÓÚÜ]ST)(?P<s2_R3c>[B-DF-HJ-ÑP-TV-Z][AEIOUÁÉÍÓÚÜ]))|' \
                 r'(?P<R3d>(?P<s1_R3d>[AEIOUÁÉÍÓÚÜ]NC)(?P<s2_R3d>T[AEIOUÁÉÍÓÚÜ]))|' \
                 r'(?P<R4>(?P<s1_R4>[AEIOUÁÉÍÓÚÜ](([BDNMLR]S)|(ST)))(?P<s2_R4>[PCBGF][RL][AEIOUÁÉÍÓÚÜ])))'

#Función que separa en sílabas, recibe una palabra (string) y devuelve esa misma string con las sílabas separadas por guiones "-"
def silabar(match, palabra):
    palabra_original=palabra
    palabra_silabada=palabra
    #Mientras que la expresión regular de un match...
    while match is not None:
        temp_silaba = ""
        #Ver qué norma ha saltado (en orden de cual comprobar primero)
        if match.group('R5b'):
            agrupaciones = [["s1_R5b1","s2_R5b1"],["s1_R5b2","s2_R5b2"],["s1_R5b3","s2_R5b3"],["s1_R5b4","s2_R5b4"],
                            ["s1_R5b5","s2_R5b5"],["s1_R5b6","s2_R5b6"],["s1_R5b7","s2_R5b7"],["s1_R5b8","s2_R5b8"],
                            ["s1_R5b9","s2_R5b9"]]
            for agrupacion in agrupaciones:
                s1 = match.group(agrupacion[0])
                s2 = match.group(agrupacion[1])
                if s1 and s2:
                    temp_silaba += f"{s1}-{s2}"
                    break
        elif match.group('R1'):
            temp_silaba += f"{match.group('s1_R1')}-{match.group('s2_R1')}"
        elif match.group('R2a'):
            temp_silaba += f"{match.group('s1_R2a')}-{match.group('s2_R2a')}"
        elif match.group('R2b'):
            temp_silaba += f"{match.group('s1_R2b')}-{match.group('s2_R2b')}"
        elif match.group('R2c1'):
            temp_silaba += f"{match.group('s1_R2c1')}-{match.group('s2_R2c1')}"
        elif match.group('R2c2'):
            temp_silaba += f"{match.group('s1_R2c2')}-{match.group('s2_R2c2')}"
        elif match.group('R3a'):
            temp_silaba += f"{match.group('s1_R3a')}-{match.group('s2_R3a')}"
        elif match.group('R3b'):
            temp_silaba += f"{match.group('s1_R3b')}-{match.group('s2_R3b')}"
        elif match.group('R3c'):
            temp_silaba += f"{match.group('s1_R3c')}-{match.group('s2_R3c')}"
        elif match.group('R3d'):
            temp_silaba += f"{match.group('s1_R3d')}-{match.group('s2_R3d')}"
        elif match.group('R4'):
            temp_silaba += f"{match.group('s1_R4')}-{match.group('s2_R4')}"

        #Si es la primera vez que se recorre la palabra, se le quita el primer match menos la última letra
        if palabra == palabra_original:
            palabra = palabra.replace(temp_silaba.replace("-","")[:-1],"")
        #En caso contrario, hace lo mismo pero quitando la primera (residuo de la iteración anterior)
        else:
            palabra = palabra.replace(temp_silaba.replace("-", "")[:-1], "")[1:]
        #Se vuelve a buscar en la palabra
        match = regex.search(patron_separacion_silabas, palabra)
        palabra_silabada=palabra_silabada.replace(temp_silaba.replace("-",""),temp_silaba)
        #Se modifica la palabra base para separar por sílabas


    return palabra_silabada


#Si se ejecuta este archivo como main, la palabra en la variable "palabra" se imprimirá separada por sílabas
if __name__ == '__main__':
    
    palabra = "cuatro"
    silabas = ""
    match = regex.search(patron_separacion_silabas, palabra)

    silabas = silabar(match,palabra)
    print(silabas)





