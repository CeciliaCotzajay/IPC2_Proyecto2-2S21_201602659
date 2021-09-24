class Cola_ComponentesEnsamblar:

    def __init__(self):
        self.items = []

    def encolar(self, componeneteEnsamblar):
        self.items.append(componeneteEnsamblar)

    def desencolar(self):
        try:
            return self.items.pop(0)
        except:
            raise ValueError("La cola de Componentes de Brazo a Ensamblar está Vacía..")