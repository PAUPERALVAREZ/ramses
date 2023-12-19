#! /usr/bin/python3

import tqdm
from euclideo import Euclideo
from gaussiano import Gaussiano
from util import *
from prm import *
from mar import *

def entorch(ficMod, ficIni, dirMar, dirPrm, ficLisUni, *guiSen):
    """
    Entrena los modelos acústicos de las unidades encontradas en los ficheros de
    entrenamiento, indicados en el fichero guía 'guiSen' escribiendo el resultado en
    el directorio 'dirMod'.

    Los ficheros de señal parametrizada se leen del directorio 'dirPrm' y el contenido
    fonético se extrae del cuarto campo de la etiqueta LBO de los ficheros de marcas
    ubicados en 'dirMar'.
    """

    # Construimos o leemos el modelo inicial
    modelo = Gaussiano(ficIni, ficLisUni)

    # Inicializamos las estructuras necesarias para acumular en ellas los datos de las
    # señales de entrenamiento.
    modelo.initEnt()

    # Bucle para todas las señales que forman el lote de entrenamiento
    for sen in tqdm.tqdm(leeLis(*guiSen)):
        # Cargamos los datos de la señal de entrenamiento
        pathMar = pathName(dirMar, sen, '.mar')
        mod = cogeTrn(pathMar)

        pathPrm = pathName(dirPrm, sen, '.prm')
        prm = leePrm(pathPrm)

        # Incorporamos la información de la señal al entrenamiento del modelo
        modelo.__add__(mod, prm)

    # Recalculamos el modelo a partir de los datos recopilados de las señales
    modelo.recalMod()

    # Inicializamos las estructuras necesarias para acumular en ellas los datos de las
    # señales de evaluación.
    modelo.initEval()
    # Bucle para todas las señales que forman el lote de evaluación
    for sen in tqdm.tqdm(leeLis(*guiSen)):
        # Cargamos los datos de la señal de evaluación
        pathMar = pathName(dirMar, sen, '.mar')
        mod = cogeTrn(pathMar)

        pathPrm = pathName(dirPrm, sen, '.prm')
        prm = leePrm(pathPrm)

        # Incorporamos la información de la señal a la evaluación del lote
        modelo.addEval(mod, prm)

    # Recalculamos la información de evaluación
    modelo.recaEval()

    # Mostramos en pantalla el resultado de la evaluación
    modelo.printEval()

    # Escribimos el modelo resultante
    chkPathName(ficMod)
    modelo.escMod(ficMod)


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
    -i PATH, --ficIni=PATH  Directorio con los modelos iniciales
    -m PATH, --ficMod=PATH  Fichero con el modelo resultante [default: .]

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
    ficMod = args['--ficMod']
    ficIni = args['--ficIni'] if '--ficIni' in args else None

    lisUni = args['<lisUni>']
    guiSen = args['<guiSen>']

    entorch(ficMod, ficIni, dirMar, dirPrm, lisUni, *guiSen)
