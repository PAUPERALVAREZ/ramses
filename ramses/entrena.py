#! /usr/bin/python3

import tqdm

from util import *
from prm import *
from mar import *

def entrena(dirMod, dirIni, dirMar, dirPrm, ficLisUni, *guiSen):
    """
    Entrena los modelos acústicos de las unidades encontradas en los ficheros de
    entrenamiento, indicados en el fichero guía 'guiSen' escribiendo el resultado en
    el directorio 'dirMod'.

    Los ficheros de señal parametrizada se leen del directorio 'dirPrm' y el contenido
    fonético se extrae del cuarto campo de la etiqueta LBO de los ficheros de marcas
    ubicados en 'dirMar'.
    """

    # Construimos o leemos el modelo inicial
    modelos = {}
    unidades = leeLis(ficLisUni)
    if dirIni:
        for unidad in unidades:
            pathMod = pathName(dirIni, unidad, '.mod')
            with open(pathMod, 'rb') as fpMod:
                modelos[unidad] = np.load(fpMod)

    # Inicializamos las estructuras necesarias para acumular en ellas los datos de las
    # señales de entrenamiento.
    sumPrm = {unidad: 0 for unidad in unidades}
    numSen = {unidad: 0 for unidad in unidades}

    # Bucle para todas las señales que forman el lote de entrenamiento
    for sen in tqdm.tqdm(leeLis(*guiSen)):
        # Cargamos los datos de la señal de entrenamiento
        pathMar = pathName(dirMar, sen, '.mar')
        mod = cogeTrn(pathMar)

        pathPrm = pathName(dirPrm, sen, '.prm')
        prm = leePrm(pathPrm)

        # Incorporamos la información de la señal al entrenamiento del modelo
        sumPrm[mod] += prm
        numSen[mod] += 1

    # Recalculamos el modelo a partir de los datos recopilados de las señales
    for unidad in unidades:
        modelos[unidad] = sumPrm[unidad] / numSen[unidad]

    # Inicializamos las estructuras necesarias para acumular en ellas los datos de las
    # señales de evaluación.
    sumPrm_2 = {unidad: 0 for unidad in unidades}
    numSen = {unidad: 0 for unidad in unidades}

    # Bucle para todas las señales que forman el lote de evaluación
    for sen in tqdm.tqdm(leeLis(*guiSen)):
        # Cargamos los datos de la señal de evaluación
        pathMar = pathName(dirMar, sen, '.mar')
        mod = cogeTrn(pathMar)

        pathPrm = pathName(dirPrm, sen, '.prm')
        prm = leePrm(pathPrm)

        # Incorporamos la información de la señal a la evaluación del lote
        sumPrm_2[mod] += prm ** 2
        numSen[mod] += 1

    # Recalculamos la información de evaluación
    distancia_2 = 0
    totSen = 0
    for unidad in unidades:
        distancia_2 += numSen[unidad] * (sumPrm_2[unidad] / numSen[unidad] - modelos[unidad])
        totSen += numSen[unidad]

    distancia = (np.sum(distancia_2) / totSen) ** 0.5

    # Mostramos en pantalla el resultado de la evaluación
    print(f'{distancia = :.2f}')

    # Escribimos el modelo resultante
    for unidad in unidades:
        pathMod = pathName(dirMod, unidad, '.mod')
        chkPathName(pathMod)
        with open(pathMod, 'wb') as fpMod:
            np.save(fpMod, modelos[unidad])


#################################################################################
# Invocación en línea de comandos
#################################################################################

if __name__ == '__main__':
    from docopt import docopt
    import sys

    Sinopsis = f"""
Entrena los modelos acústicos a partir de una base de datos de entrenamiento

Usage:
    {sys.argv[0]} [options] <lisUni> <guiSen>...
    {sys.argv[0]} -h | --help
    {sys.argv[0]} --version

Opciones:
    -p PATH, --dirPrm=PATH  Directorio con las señales parametrizadas [default: .]
    -a PATH, --dirMar=PATH  Directorio con los ficheros de marcas [default: .]
    -i PATH, --dirIni=PATH  Directorio con los modelos iniciales
    -m PATH, --dirMod=PATH  Directorio con los modelos resultantes [default: .]

Argumentos:
    <lisUni>   Fichero con la lista de unidades fonéticas.
    <guiSen>   Nombre del fichero guía con los nombres de las señales usadas en el
               entrenamiento. Pueden especificarse tantos ficheros guía como sea
               necesario.

Entrenamiento:
    El programa lee los contenidos fonéticos de los ficheros de marcas y entrena los
    modelos de las unidades fonéticas encontradas en ellos.
"""

    args = docopt(Sinopsis, version=f'{sys.argv[0]}: Ramses v3.4 (2020)')

    dirPrm = args['--dirPrm']
    dirMar = args['--dirMar']
    dirMod = args['--dirMod']
    dirIni = args['--dirIni'] if '--dirIni' in args else None

    lisUni = args['<lisUni>']
    guiSen = args['<guiSen>']

    entrena(dirMod, dirIni, dirMar, dirPrm, lisUni, *guiSen)
