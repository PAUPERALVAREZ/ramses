#! /usr/bin/python3

import tqdm

from util import *
from prm import *

def reconoce(dirRec, dirPrm, dirMod, ficLisMod, *guiSen):
    """
    Determina la unidad cuyo modelo se ajusta mejor a cada señal a reconocer y escribe
    su nombre en el cuarto campo de una etiqueta LBO de un fichero de marcas ubicado
    en el directorio 'dirRec' y del mismo nombre que la señal, pero con extensión '.rec'.

    Las unidades a reconocer se enumeran en el fichero 'ficLisMod', y sus modelos
    deben estar en el directorio 'dirMod'. Se reconocen las señales indicadas por el
    fichero guía 'guiSen', que deben estar en el directorio 'dirPrm'.
    """
    
    modelos = {}
    for mod in leeLis(ficLisMod):
        pathMod = pathName(dirMod, mod, '.mod')
        with open(pathMod, 'rb') as fpMod:
            modelos[mod] = np.load(fpMod)

    for sen in tqdm.tqdm(leeLis(*guiSen)):
        pathPrm = pathName(dirPrm, sen, '.prm')
        prm = leePrm(pathPrm)

        minDist = np.inf
        for mod in modelos:
            dist = sum(abs(prm - modelos[mod]) ** 2)
            if dist < minDist:
                minDist = dist
                rec = mod

        pathRec =  pathName(dirRec, sen, '.rec')
        chkPathName(pathRec)
        with open(pathRec, 'wt') as fpRec:
            fpRec.write(f'LBO: ,,,{rec}\n')


#################################################################################
# Invocación en línea de comandos
#################################################################################

if __name__ == '__main__':
    from docopt import docopt
    import sys

    Sinopsis = f"""
Reconoce una base de datos de señales parametrizadas

Usage:
    {sys.argv[0]} [options] --lisMod=FILE <guiSen>...
    {sys.argv[0]} -h | --help
    {sys.argv[0]} --version

Opciones:
    -r PATH, --dirRec=PATH  Directorio con los ficheros del resultado [default: .]
    -p PATH, --dirPrm=PATH  Directorio con las señales parametrizadas [default: .]
    -m PATH, --dirMod=PATH  Directorio con los modelos acústicos [default: .]
    -l FILE, --lisMod=FILE  Fichero con la lista de unidades a reconocer

Argumentos:
    <guiSen>  Nombre del fichero guía con los nombres de las señales a reconocer.
              Pueden especificarse tantos ficheros guía como sea necesario.
"""

    args = docopt(Sinopsis, version=f'{sys.argv[0]}: Ramses v3.4 (2020)')

    dirRec = args['--dirRec']
    dirPrm = args['--dirPrm']
    dirMod = args['--dirMod']
    ficLisMod = args['--lisMod']

    guiSen = args['<guiSen>']

    reconoce(dirRec, dirPrm, dirMod, ficLisMod, *guiSen)
