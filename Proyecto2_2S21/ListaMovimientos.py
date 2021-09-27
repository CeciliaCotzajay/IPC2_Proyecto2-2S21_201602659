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

    def buscarPorSegundo(self, seg):
        movimiento = None
        actual = self.primero
        if self.tam != 0:
            while actual is not None:
                if actual.Movimiento.noSegundo == seg:
                    movimiento = actual.Movimiento
                actual = actual.siguiente
        return movimiento
