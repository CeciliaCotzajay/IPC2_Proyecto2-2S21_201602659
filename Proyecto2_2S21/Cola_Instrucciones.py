class Cola_Instrucciones:

    def __init__(self):
        self.items = []

    def encolar(self, instruccion):
        self.items.append(instruccion)

    def desencolar(self):
        try:
            return self.items.pop(0)
        except:
            print("La cola de Instrucciones está Vacía..")
            return None

    def devolverTam(self):
        return len(self.items)

    def retornarPrimero(self):
        try:
            return self.items[0]
        except:
            print("La cola de Instrucciones está Vacía..")
            return None

    def cambiarEstadoInstruccion(self, instruccion):
        idInstruBuscar = instruccion.idInstruccion
        for i in self.items:
            if i.idInstruccion == idInstruBuscar:
                i.estadoInstruccion = "lista"

