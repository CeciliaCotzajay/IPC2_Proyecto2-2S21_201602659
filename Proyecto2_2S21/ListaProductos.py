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

    def buscarNombre(self, nombre):
        producto = None
        actual = self.primero
        if self.tam != 0:
            while actual is not None:
                if actual.Producto.nombre == nombre:
                    producto = actual.Producto
                actual = actual.siguiente
        return producto
