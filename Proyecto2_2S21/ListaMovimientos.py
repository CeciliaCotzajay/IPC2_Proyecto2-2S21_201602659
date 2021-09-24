from NodoMovimiento import NodoMovimiento


class ListaMovimientos:

    def __init__(self):
        self.primero = None
        self.tam = 0

    def insertar(self, movimiento):
        nuevo = NodoMovimiento(Movimiento=movimiento)
        if self.tam == 0:
            self.primero = nuevo
            self.tam += 1
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
            self.tam += 1