class Instruccion:

    def __init__(self, idInstruccion, idBrazo=None, componente=None):
        self.idInstruccion = idInstruccion
        self.noLinea = idBrazo
        self.componente = componente
