import numpy as np

def escrPrm(pathPrm, prm):
    """
    Escribe la señal parametrizada 'prm' en el fichero 'pathPrm'.
    """

    with open(pathPrm, 'wb') as fpPrm:
        np.save(fpPrm, prm)


def leePrm(pathPrm):
    """
    Devuelve la señal parametrizada contenida en el fichero 'pathPrm'.
    """

    with open(pathPrm, 'rb') as fpPrm:
        return np.load(fpPrm)

