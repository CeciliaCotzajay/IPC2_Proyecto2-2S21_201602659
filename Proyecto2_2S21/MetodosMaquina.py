import re
import webbrowser
from xml.dom import minidom
import xml.etree.cElementTree as ET
import copy
import prettify

from Brazo import Brazo
from Cola_ComponentesEnsamblar import Cola_ComponentesEnsamblar
from Cola_Instrucciones import Cola_Instrucciones
from Instruccion import Instruccion
from ListaBrazos import ListaBrazos
from ListaProductos import ListaProductos
from ListaSimple import ListaSimple
from Producto import Producto
from Simulación import Simulacion


class MetodosMaquina:
    listaSimulaciones = None
    listaGeneralBrazos = None
    listaProductos = None
    cadenaEscritura = ""

    def cargarAjustesMaquina(self, rutaArchivo):
        docXML = minidom.parse(rutaArchivo)
        maquina = docXML.getElementsByTagName("Maquina")[0]
        cantlinprod = maquina.getElementsByTagName("CantidadLineasProduccion")[0]
        cantLineasProd = int(cantlinprod.firstChild.data)
        if 0 < cantLineasProd < 100:
            self.listaGeneralBrazos = ListaBrazos()
            listadoLineasProduccion = maquina.getElementsByTagName("ListadoLineasProduccion")[0]
            lineaProduccion = listadoLineasProduccion.getElementsByTagName("LineaProduccion")
            for lineaProd in lineaProduccion:
                numeroLinea = lineaProd.getElementsByTagName("Numero")[0]
                idLinea = int(numeroLinea.firstChild.data)
                if 0 < idLinea < cantLineasProd + 1:
                    cantcomponen = lineaProd.getElementsByTagName("CantidadComponentes")[0]
                    cantComponentes = int(cantcomponen.firstChild.data)
                    if 1000 > cantComponentes > 0:
                        tiemEnsam = lineaProd.getElementsByTagName("TiempoEnsamblaje")[0]
                        tiempoEnsamble = int(tiemEnsam.firstChild.data)
                        if tiempoEnsamble > 0:
                            brazo = Brazo("L"+str(idLinea), "C"+str(cantComponentes), tiempoEnsamble, None, None)
                            self.listaGeneralBrazos.insertar(brazo)
                        else:
                            print("El Timempo de Ensamblaje debe ser mayor a 0")
                    else:
                        print("El número de Cantidad de Componentes debe ser menor a 1000")
                else:
                    print(
                        "El número de la Línea de Producción NO es mayor a 0")
            print(self.listaGeneralBrazos.tam)
            if self.listaGeneralBrazos.tam != cantLineasProd:
                self.listaGeneralBrazos = None
                print("E2: La cantidad de Líneas de Producción no cumple con el tamaño..")
            lisProductos = maquina.getElementsByTagName("ListadoProductos")[0]
            Productos = lisProductos.getElementsByTagName("Producto")
            p = 0
            self.listaProductos = ListaProductos()
            for produc in Productos:
                p += 1
                nombrePro = produc.getElementsByTagName("nombre")[0]
                nombreProducto = str(nombrePro.firstChild.data)
                elabor = produc.getElementsByTagName("elaboracion")[0]
                elaboracion = str(elabor.firstChild.data)
                ER_elaboracion = re.findall('L[\d]{1,3}pC[\d]{1,3}', elaboracion)
                if len(ER_elaboracion) == 0:
                    print("Error al leer con ER")
                else:
                    colaInstrucciones = Cola_Instrucciones()
                    i = 0
                    for e in ER_elaboracion:
                        i += 1
                        ins = str(e).split("p")
                        idbrazo = ins[0]
                        componente = ins[1]
                        instruccion = Instruccion(i, idbrazo, componente, None, None)
                        colaInstrucciones.encolar(instruccion)
                    producto = Producto(p, nombreProducto, colaInstrucciones)
                    # print(colaInstrucciones.devolverTam())
                    self.listaProductos.insertar(producto)
        else:
            print("E1: La cantidad de Líneas de Producción no cumple con el tamaño..")
        print(self.listaGeneralBrazos.tam)
        print(self.listaProductos.tam)

    def cargarMasivaProductos(self, rutaArchivo):
        self.listaSimulaciones = ListaSimple()
        docXML = minidom.parse(rutaArchivo)
        simulacion = docXML.getElementsByTagName("Simulacion")[0]
        nombreSim = simulacion.getElementsByTagName("Nombre")[0]
        nombreSimulacion = str(nombreSim.firstChild.data)
        lisProductos = simulacion.getElementsByTagName("ListadoProductos")[0]
        Productos = lisProductos.getElementsByTagName("Producto")
        for producto in Productos:
            nombreProducto = str(producto.firstChild.data)
            print(nombreProducto)
            productoEncontrado = self.listaProductos.buscarNombre(nombreProducto)
            if productoEncontrado is None:
                print("Producto: " + nombreProducto + " No encontrado...")
            else:
                liBrazos = copy.deepcopy(self.listaGeneralBrazos)
                productoEncon = copy.deepcopy(productoEncontrado)
                simulacion = Simulacion(nombreSimulacion, "noListo", productoEncon, liBrazos)
                self.listaSimulaciones.insertar(simulacion)
                self.listaSimulaciones.setearComponentesEnsamblar(nombreSimulacion)
        print(self.listaSimulaciones.tam)

    def generarXMLsalida(self, nombre):
        salidaSimulacion = ET.Element('SalidaSimulacion')
        nombreSalida = ET.SubElement(salidaSimulacion, "Nombre")
        nombreArchivoSalida = 'nombreSalidaCualquiera:)'
        nombreSalida.text = nombreArchivoSalida
        listaProductos = ET.SubElement(salidaSimulacion, 'ListadoProductos')
        # POR CADA PRODUCTO
        producto = ET.SubElement(listaProductos, 'Producto')
        nombreP = ET.SubElement(producto, 'Nombre')
        nombreP.text = 'nombreProducto'
        tiempoTotal = ET.SubElement(producto, 'TiempoTotal')
        tiempoTotal.text = '>0000024'
        elaboracionOptima = ET.SubElement(producto, 'ElaboracionOptima')
        # POR CADA TIEMPO, POR CADA SEGUNDO
        tiempo = ET.SubElement(elaboracionOptima, 'Tiempo')
        tiempo.set('NoSegundo', '24')
        # POR CADA LINEA_ENSAMBLAJE
        lineaEnsamblaje = ET.SubElement(tiempo, 'LineaEnsamblaje')
        lineaEnsamblaje.set('NoLinea', '24En')

        datos = ET.tostring(salidaSimulacion, encoding="'utf-8'")
        datos2 = minidom.parseString(datos)
        texto = datos2.toprettyxml(indent='\t', encoding="'utf-8'")
        texto2 = texto.decode('utf-8')
        archivoXML = open(nombreArchivoSalida + '.xml', 'wb')
        archivoXML.write(texto2)

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
