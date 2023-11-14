import regex as re
import csv

def entonacion(palabra,regla_silaba,regla_vocal):
    #aplica la norma a cada sílaba para ver si hay una tilde (descarta esdrújulas y sobreesdrújulas)
    for silaba in palabra:

        tildes=regla_silaba.match(silaba.rstrip()).group("R1")
        #si encuentra, la reemplaza por su mayúscula y devuelve la palabra
        if(tildes!=""):
            regla_silaba.sub(tildes.toupper(),tildes)
            return palabra
    #si no, intenta ver si la palabra es llana, si lo es, le aplica las normas de los diptongos y triptongos (descarta llanas)
    llana=regla_silaba.match(palabra[::-2].rstrip()).group("R2")
    if(llana!=""):
        vocales=0;
        for letra in palabra[::-2]:
            if letra in ("a","e","i","o","u"):
                vocales+=1
        if (vocales==3):
            segunda=False
            for letra in silaba:
                if (letra in ("a","e","i","o","u")):
                    if segunda:
                        palabra[::-2][letra] = letra.toupper()
                        break
                    else: segunda = True
        elif (vocales==2):
            tonica = regla_vocal.match(palabra[::-2].rstrop()).group("R4a")
            if (tonica != ""):
                regla_vocal.sub(tonica.toupper(),tonica)
                return palabra
            else:
                tonica = regla_vocal.match(palabra[::-2].rstrop()).group("R4b")
                regla_vocal.sub(tonica.toupper(), tonica)
                return palabra
        else:
            for letra in palabra[::-2]:
                if letra in ("a","e","i","o","u"):
                    palabra[::-2][letra] = letra.toupper()
                    return palabra
    else: #si no se cumple ninguna condición anterior, la palabra tiene que ser aguda, y se hace de vuelta lo anterior pero en la última sílaba
        vocales = 0;
        for letra in palabra[::-1]:
            if letra in ("a", "e", "i", "o", "u"):
                vocales += 1
        if (vocales == 3):
            segunda = False
            for letra in silaba:
                if (letra in ("a", "e", "i", "o", "u")):
                    if segunda:
                        palabra[::-2][letra] = letra.toupper()
                        break
                    else:
                        segunda = True
        elif (vocales == 2):
            tonica = regla_vocal.match(palabra[::-1].rstrop()).group("R4a")
            if (tonica != ""):
                regla_vocal.sub(tonica.toupper(), tonica)
                return palabra
            else:
                tonica = regla_vocal.match(palabra[::-1].rstrop()).group("R4b")
                regla_vocal.sub(tonica.toupper(), tonica)
                return palabra
        else:
            for letra in palabra[::-2]:
                if letra in ("a", "e", "i", "o", "u"):
                    palabra[::-2][letra] = letra.toupper()
                    return palabra








def silabar(palabra,regla_silabacion):
    pass

def procesar(reglas, entrada):
    #quitar palabras repetidas
    conjuntoEntrada = set(entrada.split('\n'))

    #todo escribir en un archivo de texto

    #escribir en un archivo de salida si ya existe
    archivo = open('salida.cvs','a+')
    escritor = csv.writer(archivo)
    lector = csv.reader(archivo)
    #si se acaba de crear, añadirle la cabecera
    if (len(list(lector)) == 0):
        escritor.writerow(['Palabra', 'Silabación', 'Entonación']);

    palabras = []
    #lee desde la segunda linea (la primera es la cabecera)
    try:
        for palabra in next(lector):
            palabras.append(palabra[0])
    except StopIteration:
        pass



    for palabra_entrada in conjuntoEntrada:
        if palabra_entrada not in palabras:# ver si la palabra ya está
            palabra_silabada= silabar(palabra_entrada,reglas[0])
            palabra_entonada= entonacion(palabra_silabada,reglas[1],reglas[2])
            escritor.writerow([palabra_entrada,palabra_silabada , palabra_entonada])











    #leer fichero, separar en su totalidad en una lista y quedarnos con las palabras normales







if __name__ == '__main__':
    patron_silabas = r''
    reglas_silabas = re.compile(patron_silabas)
    patron_entonacion_silabas=r'(?P<R1> [áéíóú])|(?P<R2> *[snaeiou]$)|(?P<R3> *[qwrtypdfghjklñzxcvbm]$)'
    reglas_entonacion_silabas = re.compile(patron_entonacion_silabas)
    patron_vocal_tonica= r'(?P<R4>(?P<R4a> [aeo])|(?P<R4b> [iu][iu]))'
    reglas_vocal_tonica = re.compile(patron_vocal_tonica)
    reglas =[reglas_silabas,reglas_entonacion_silabas,reglas_vocal_tonica]

    try: #leer archivo de texto con las palabras de entrada
        entrada = open('vocabulario.txt','r')
    except FileNotFoundError: #si no encuentra archivo, leer desde teclado las palabras
        entrada = ""
        ultima_entrada = ""
        while (True):
            ultima_entrada = str(input("Introduce las palabras que quieres procesar una a una separadas por un enter. Si quieres terminar pon 0: "))
            if ultima_entrada == "<exit>":
                break
            entrada +=ultima_entrada + "\n"

    procesar(reglas,entrada)