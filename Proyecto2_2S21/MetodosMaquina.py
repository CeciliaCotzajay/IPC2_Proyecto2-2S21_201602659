import webbrowser


class MetodosMaquina:
    cadenaEscritura = ""

    def mostrarDocumentacion(self):
        ruta = str("C:\\Users\\Maria\\Documents\\GitHub\\IPC2_Proyecto1_201602659_Jun\\[IPC2]Proyecto_2_2S2021.pdf")
        webbrowser.open_new(ruta)

    def mostrarReporteHTML(self):
        # ---------------------------------------------------------
        # ESTA LINEA SERÁ ELIMINADA Y  SERÁ CONVERTIDA EN PARAMETRO
        nombre = "ReporteHTML"
        # ---------------------------------------------------------
        self.crearArchivoHTML(nombre)
        self.escribirLineaHTML(nombre)
        webbrowser.open_new_tab("C:\\Users\\Maria\\Desktop\\" + nombre + ".html")

    def crearArchivoHTML(self, nombre):
        archivo = open("C:\\Users\\Maria\\Desktop\\" + nombre + ".html", "w")
        archivo.close()

    def escribirLineaHTML(self, nombre):
        lineaInicial = """<html>"""
        # ---------------------------------------------------------
        # ESTA LINEA SERÁ ELIMINADA Y  SERÁ CONVERTIDA EN PARAMETRO
        linea = """<br><br><center><p>Hola a todos!!! :)</p></center><br>"""
        # ---------------------------------------------------------
        self.cadenaEscritura += linea
        lineafinal = """</html>"""
        unificado = lineaInicial + self.cadenaEscritura + lineafinal
        archivo = open("C:\\Users\\Maria\\Desktop\\" + nombre + ".html", "a")
        archivo.write(unificado)
        archivo.close()