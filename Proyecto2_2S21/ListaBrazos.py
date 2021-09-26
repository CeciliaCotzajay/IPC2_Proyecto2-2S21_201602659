from Cola_ComponentesEnsamblar import Cola_ComponentesEnsamblar
from NodoBrazo import NodoBrazo


class ListaBrazos:

    def __init__(self):
        self.primero = None
        self.tam = 0

    def insertar(self, Brazo):
        nuevo = NodoBrazo(brazo=Brazo)
        if self.tam == 0:
            self.primero = nuevo
            self.tam += 1
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
            self.tam += 1

    def setearComponenteEnsambra(self, idbrazo, componente):
        actual = self.primero
        if self.tam != 0:
            while actual is not None:
                if actual.brazo.idBrazo == idbrazo:
                    if actual.brazo.colaComponentesEnsamblar is None:
                        colaComponenteEnsamblar = Cola_ComponentesEnsamblar()
                        colaComponenteEnsamblar.encolar(componente)
                        actual.brazo.colaComponentesEnsamblar = colaComponenteEnsamblar
                    else:
                        actual.brazo.colaComponentesEnsamblar.encolar(componente)
                actual = actual.siguiente

    def imprimirComponenetesEnsamblar(self):
        if self.tam == 0:
            print("----->No hay Brazos en lista!!")
        else:
            actual = self.primero
            while actual is not None:
                print("***", actual.brazo.idBrazo, "***")
                actual.brazo.colaComponentesEnsamblar.imprimir()
                actual = actual.siguiente
