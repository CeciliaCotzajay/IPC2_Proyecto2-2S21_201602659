class Instruccion:

    def __init__(self, idInstruccion, idBrazo=None, componente=None, estadoInstruccion=None, segundoListo=None):
        self.idInstruccion = idInstruccion
        self.noLinea = idBrazo
        self.componente = componente
        self.estadoInstruccion = estadoInstruccion
        self.segundoListo = segundoListo
