import regex

patron_separacion_silabas = r'(?i)((?<R5b>((?P<s1_R5b1>[AEO])(?P<s2_R5b1>H?[ÚÍ]))|((?P<s1_R5b2>[ÚÍ])(?P<s2_R5b2>H?[AEO]))|((?P<s1_R5b3>[AÁ])(?P<s2_R5b3>H?[AÁ]))|((?P<s1_R5b4>[EÉ])(?P<s2_R5b4>H?[EÉ]))|((?P<s1_R5b5>[IÍ])(?P<s2_R5b5>H?[IÍ]))|((?P<s1_R5b6>[OÓ])(?P<s2_R5b6>H?[OÓ]))|((?P<s1_R5b7>[UÚ])(?P<s2_R5b7>H?[UÚ]))|((?P<s1_R5b8>[AEOÁÉÓ])(?P<s2_R5b8>H?[AEO]))|((?P<s1_R5b9>[AEO])(?P<s2_R5b9>H?[AEOÁÉÓ])))|' \
                            r'(?P<R1>(?P<s1_R1>[AEIOUÁÉÍÓÚÜ])(?P<s2_R1>(CH|LL|RR|[BCDFGJKLMNÑPQRSTVWXYZ])([AEIOUÁÉÍÓÚÜ]|Y$)))|' \
                            r'(?P<R2a>(?P<s1_R2a>[AEIOUÁÉÍÓÚÜ])(?P<s2_R2a>([PCBGF])([RL])[AEIOUÁÉÍÓÚÜ]))|' \
                            r'(?P<R2b>(?P<s1_R2b>[AEIOUÁÉÍÓÚÜ])(?P<s2_R2b>([DT])([R])[AEIOUÁÉÍÓÚÜ]))|' \
                            r'(?P<R2c1>(?P<s1_R2c1>[AEIOUÁÉÍÓÚÜ][DHJKLMNÑQRSTVWXYZ])(?P<s2_R2c1>(LL|CH|[BCDFGHJKLMNÑPQRSTVWXYZ])[AEIOUÁÉÍÓÚÜ]))|' \
                            r'(?P<R2c2>(?P<s1_R2c2>[AEIOUÁÉÍÓÚÜ][BCDFGHJKLMNÑPQRSTVWXYZ])(?P<s2_R2c2>(LL|CH|[BCDFGHJKMNÑPQSTVWXYZ])[AEIOUÁÉÍÓÚÜ]))|' \
                            r'(?P<R2c3>(?P<s1_R2c3>[AEIOUÁÉÍÓÚÜ][BCFGHJKLMNÑPQRSVWXYZ])(?P<s2_R2c3>(LL|CH|[BCDFGHJKLMNÑPQRSTVWXYZ])[AEIOUÁÉÍÓÚÜ]))|' \
                            r'(?P<R2c4>(?P<s1_R2c4>[AEIOUÁÉÍÓÚÜ][BCDFGHJKLMNÑPQRSTVWXYZ])(?P<s2_R2c4>(LL|CH|[BCDFGHJKLMNÑPQSTVWXYZ])[AEIOUÁÉÍÓÚÜ]))|' \
                            r'(?P<R3a>(?P<s1_R3a>[AEIOUÁÉÍÓÚÜ][B-DF-HJ-NP-TV-ZÑ])(?P<s2_R3a>(([PCBGF][RL])|([DT][R]))[AEIOUÁÉÍÓÚÜ]))|' \
                            r'(?P<R3b>(?P<s1_R3b>[AEIOUÁÉÍÓÚÜ][BDNMLR]S)(?P<s2_R3b>[B-DF-HJ-ÑP-TV-Z][AEIOUÁÉÍÓÚÜ]))|' \
                            r'(?P<R3c>(?P<s1_R3c>[AEIOUÁÉÍÓÚÜ]ST)(?P<s2_R3c>[B-DF-HJ-ÑP-TV-Z][AEIOUÁÉÍÓÚÜ]))|' \
                            r'(?P<R3d>(?P<s1_R3d>[AEIOUÁÉÍÓÚÜ]NC)(?P<s2_R3d>T[AEIOUÁÉÍÓÚÜ]))|' \
                            r'(?P<R4>(?P<s1_R4>[AEIOUÁÉÍÓÚÜ](([BDNMLR]S)|(ST)))(?P<s2_R4>[PCBGF][RL][AEIOUÁÉÍÓÚÜ])))'

automata_silabas = regex.compile(patron_separacion_silabas)


def silabar(palabra):
    pos = 0
    cortes = [0]
    match = automata_silabas.search(palabra, pos)
    while match:

        if match.group('R5b'):
            cortes.append(match.start() + 1)
        elif match.group('R1'):
            cortes.append(match.start() + 1)
        elif match.group('R2a'):
            cortes.append(match.start() + 1)
        elif match.group('R2b'):
            cortes.append(match.start() + 1)
        elif match.group('R2c1'):
            cortes.append(match.start() + 2)
        elif match.group('R2c2'):
            cortes.append(match.start() + 2)
        elif match.group('R2c3'):
            cortes.append(match.start() + 2)
        elif match.group('R2c4'):
            cortes.append(match.start() + 2)
        elif match.group('R3a'):
            cortes.append(match.start() + 2)
        elif match.group('R3b'):
            cortes.append(match.start() + 3)
        elif match.group('R3c'):
            cortes.append(match.start() + 3)
        elif match.group('R3d'):
            cortes.append(match.start() + 3)
        elif match.group('R4'):
            cortes.append(match.start() + 3)
        pos = match.end() - 1
        match = automata_silabas.search(palabra, pos)
    silabas = []
    inicio = 0
    for corte in cortes[1:]:
        silabas.append(palabra[inicio:corte])
        inicio = corte
    silabas.append(palabra[inicio:])
    return silabas


if __name__ == '__main__':
    entrada = None

    while entrada not in ("1", "2", "3"):
        print("---EJECUTANDO TEST DE FRAGMENTO DE SILABACIÓN---\n1. Silabar palabras escritas por teclado.\n2. Silabar"
              "palabras del fichero vocabuario.txt\n3. Salir\n")

        entrada = str(input("Elige la opción que quieres escribiendo su número: "))
        match entrada:
            case "1":
                palabra = ""
                while palabra != "0":
                    palabra = str(input("Introduce la palabra que quieres silabar, procura que esté bien escrita."
                                        " Pon un 0 para terminar: "))
                    if palabra != "0":
                        print(silabar(palabra))

                break
            case "2":
                with open('vocabulario.txt', 'r', encoding='utf-8') as f:
                    # Leemos cada línea del archivo
                    for linea in f:
                        # Eliminamos los espacios y tabulaciones
                        linea = linea.replace(' ', '').replace('\t', '').replace('\n', '')
                        print(silabar(linea))
                f.close()
                break
            case "3":
                break
            case _:
                print("Por favor, inserta un valor entre 1 y 3")
