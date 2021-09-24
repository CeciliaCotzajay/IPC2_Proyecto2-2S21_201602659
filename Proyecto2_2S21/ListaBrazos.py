class ListaBrazos:

    def __init__(self):
        self.primero = None
        self.tam = 0

    def insertar(self, noombre, matrizOrto):
        nuevo = Nodo(nombre=noombre, MatrizOrtogonal=matrizOrto)
        if self.tam == 0:
            self.primero = nuevo
            self.tam += 1
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
            self.tam += 1
