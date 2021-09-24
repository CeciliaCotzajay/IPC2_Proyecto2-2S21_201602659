from NodoProducto import NodoProducto


class ListaProductos:

    def __init__(self):
        self.primero = None
        self.tam = 0

    def insertar(self, producto):
        nuevo = NodoProducto(Producto=producto)
        if self.tam == 0:
            self.primero = nuevo
            self.tam += 1
        else:
            actual = self.primero
            while actual.siguiente:
                actual = actual.siguiente
            actual.siguiente = nuevo
            self.tam += 1
