import webbrowser
from xml.dom import minidom
import xml.etree.cElementTree as ET
import prettify


class MetodosMaquina:
    cadenaEscritura = ""

    def cargarAjustesMaquina(self, rutaArchivo):
        docXML = minidom.parse(rutaArchivo)
        maquina = docXML.getElementsByTagName("Maquina")[0]
        cantlinprod = maquina.getElementsByTagName("CantidadLineasProduccion")[0]
        cantLineasProd = int(cantlinprod.firstChild.data)
        listadoLineasProduccion = maquina.getElementsByTagName("ListadoLineasProduccion")
        for lineaProd in listadoLineasProduccion:
            numeroLinea = lineaProd.getElementsByTagName("Numero")[0]
            idLinea = int(numeroLinea.firstChild.data)
            cantcomponen = lineaProd.getElementsByTagName("CantidadComponentes")[0]
            cantComponentes = int(cantcomponen.firstChild.data)
            tiemEnsam = lineaProd.getElementsByTagName("TiempoEnsamblaje")[0]
            tiempoEnsamble = int(tiemEnsam.firstChild.data)
            # AQUI SE DEBEN GUARDAR LAS LINEASSSSSSSSSSSS
        listadoProductos = maquina.getElementsByTagName("ListadoProductos")
        for Producto in listadoProductos:
            nombrePro = Producto.getElementsByTagName("nombre")[0]
            nombreProducto = str(nombrePro.firstChild.data)
            elabor = Producto.getElementsByTagName("elaboracion")[0]
            elaboracion = str(elabor.firstChild.data)
            # AQUI SE DEBEN GUARDAR LOS PRODUCTOSSSSS

    def cargarMasivaProductos(self, rutaArchivo):
        docXML = minidom.parse(rutaArchivo)
        simulacion = docXML.getElementsByTagName("Simulacion")[0]
        nombreSim = simulacion.getElementsByTagName("Nombre")[0]
        nombreSimulacion = str(nombreSim.firstChild.data)
        listadoProductos = simulacion.getElementsByTagName("ListadoProductos")
        for producto in listadoProductos:
            nombreProd = producto.getElementsByTagName("Producto")[0]
            nombreProducto = str(nombreProd.firstChild.data)
            # AQUI SE DEBEN GUARDAR LOS PRODUCTOSSSSSSSS



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
