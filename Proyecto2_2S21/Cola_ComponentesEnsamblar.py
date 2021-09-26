class Cola_ComponentesEnsamblar:

    def __init__(self):
        self.items = []
        self.tam = None

    def encolar(self, componeneteEnsamblar):
        self.items.append(componeneteEnsamblar)

    def desencolar(self):
        try:
            return self.items.pop(0)
        except:
            print("La cola de Componentes de Brazo a Ensamblar está Vacía..")
            return None

    def devolverTam(self):
        return len(self.items)

    def imprimir(self):
        for i in self.items:
            print(i)