class NodoSimple:

    def __init__(self, nombreSimulacion, idProductoEnsamblado=None, ListaBrazos=None, siguiente=None):
        self.nombreSimulacion = nombreSimulacion
        self.idProductoEnsamblado = idProductoEnsamblado
        self.ListaBrazos = ListaBrazos
        self.siguiente = siguiente
