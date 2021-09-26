from NodoSimple import NodoSimple


class ListaSimple:

    def __init__(self):
        self.primero = None
        self.tam = 0

    def insertar(self, simulacion):
        nuevo = NodoSimple(Simulacion=simulacion)
        if self.tam == 0:
            self.primero = nuevo
            self.tam += 1
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
            self.tam += 1

    def buscarNombre(self, nombre):
        simulacion = None
        actual = self.primero
        if self.tam != 0:
            while actual is not None:
                if actual.Simulacion.Nombre == nombre:
                    simulacion = actual.Simulacion
                actual = actual.siguiente
        return simulacion

    def setearComponentesEnsamblar(self, nombreSimulacion):
        simulacionEncontrada = self.buscarNombre(nombreSimulacion)
        auxColainstrucciones = simulacionEncontrada.Producto.colaInstrucciones
        auxListaBrazos = simulacionEncontrada.ListaBrazos
        for i in auxColainstrucciones.items:
            b = i.idBrazo
            c = i.componente
            auxListaBrazos.setearComponenteEnsambra(b, c)
        auxListaBrazos.imprimirComponenetesEnsamblar()