import re
import webbrowser
from xml.dom import minidom
import xml.etree.cElementTree as ET
import copy
import prettify

from Brazo import Brazo
from Cola_Instrucciones import Cola_Instrucciones
from Cola_ComponentesEnsamblar import Cola_ComponentesEnsamblar
from Instruccion import Instruccion
from ListaBrazos import ListaBrazos
from ListaMovimientos import ListaMovimientos
from ListaProductos import ListaProductos
from ListaSimple import ListaSimple
from Movimiento import Movimiento
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
                            brazo = Brazo("L" + str(idLinea), "C" + str(cantComponentes), tiempoEnsamble, None, None)
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
                        instruccion = Instruccion(i, idbrazo, componente, "noListo", None)
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
                simulacion = Simulacion(nombreSimulacion, "noListo", productoEncon, liBrazos, None)
                self.listaSimulaciones.insertar(simulacion)
                self.listaSimulaciones.setearComponentesEnsamblar(nombreSimulacion)
        print(self.listaSimulaciones.tam)

    def simularMasivamente(self):
        actual = self.listaSimulaciones.primero
        while actual is not None:
            if actual.Simulacion.estado == "noListo":
                print(actual.Simulacion.Nombre)
                print(actual.Simulacion.Producto.nombre)
                listabrazos = actual.Simulacion.ListaBrazos
                colaINSTRUCCIONES = actual.Simulacion.Producto.colaInstrucciones
                colaInstruccionesC = copy.deepcopy(colaINSTRUCCIONES)  #
                # SI ES 0 NO ESTA ENSAMBLANDO SI ES 1 SI ESTA ENSAMBLANDO
                movAnteiriorEnsamble = None
                ensamblando = 0
                contEnsamble = 0
                i = 0
                colaANTERIORdesencolar = None  # SOLO DESENCOLAR
                while colaInstruccionesC.devolverTam() > 0:
                    i += 1
                    colaANTERIORencolar = Cola_ComponentesEnsamblar()  # SOLO ENCOLAR
                    actualB = listabrazos.primero
                    while actualB is not None:
                        # ############################## PRIMERA LINEA O SEGUNDO #######################################
                        if actualB.brazo.listaMovimientos is None:
                            listaMovimiento = ListaMovimientos()
                            if actualB.brazo.colaComponentesEnsamblar is None:
                                movimiento = Movimiento("--", i)
                                listaMovimiento.insertar(movimiento)
                                colaANTERIORencolar.encolar(movimiento.estadoMovimiento)
                            else:
                                movimiento = Movimiento("C" + str(i), i)
                                listaMovimiento.insertar(movimiento)
                                colaANTERIORencolar.encolar(movimiento.estadoMovimiento)
                            actualB.brazo.listaMovimientos = listaMovimiento
                        # ################################ EL RESTO DE LINEAS ##########################################
                        else:
                            listaMovimiento = actualB.brazo.listaMovimientos
                            movimientoAnterior = colaANTERIORdesencolar.desencolar()
                            primInstruccion = colaInstruccionesC.retornarPrimero()
                            primComponenteEnsamblar = actualB.brazo.colaComponentesEnsamblar.retornarPrimero()  #
                            # SI SE ESTA ENSAMBLANDO********************************************************************
                            if ensamblando == 0:
                                # SI ESTADO ES NADA---------------------------------------------
                                if movimientoAnterior == "--":
                                    movimiento = Movimiento("--", i)
                                    listaMovimiento.insertar(movimiento)
                                    colaANTERIORencolar.encolar(movimiento.estadoMovimiento)
                                # SI ESTADO ES REPOSO------------------------------------------r
                                if movimientoAnterior == "r":
                                    movimiento = Movimiento("r", i)
                                    listaMovimiento.insertar(movimiento)
                                    colaANTERIORencolar.encolar(movimiento.estadoMovimiento)
                                # SI ESTADO ES ESPERA------------------------------------------s
                                if movimientoAnterior == "s":
                                    idBrazoInstruccion = primInstruccion.idBrazo
                                    idComponenteInstruccion = primInstruccion.componente
                                    idbrazoActual = actualB.brazo.idBrazo
                                    compoColaEnsam = actualB.brazo.colaComponentesEnsamblar.retornarPrimero()
                                    # VERIFICA SI EL COMPONENETE Y BRAZO SON LOS DE LA PRIMERA INSTRUCCION EN COLA
                                    if idbrazoActual == idBrazoInstruccion and compoColaEnsam == idComponenteInstruccion:
                                        ensamblando = 1
                                        movimiento = Movimiento("EN", i)
                                        listaMovimiento.insertar(movimiento)
                                        colaANTERIORencolar.encolar(movimiento.estadoMovimiento)
                                        contEnsamble += 1
                                    # SE QUEDA CON ESTADO ESPERA
                                    else:
                                        movimiento = Movimiento("s", i)
                                        listaMovimiento.insertar(movimiento)
                                        colaANTERIORencolar.encolar(movimiento.estadoMovimiento)
                                # SI ESTADO ES UN COMPONENTE Y EN COLA A ENSAMBLAR--------------
                                if "C" in movimientoAnterior:
                                    if movimientoAnterior == primComponenteEnsamblar:
                                        idBrazoInstruccion = primInstruccion.idBrazo
                                        idComponenteInstruccion = primInstruccion.componente
                                        idbrazoActual = actualB.brazo.idBrazo
                                        # VERIFICA SI EL COMPONENETE Y BRAZO SON LOS DE LA PRIMERA INSTRUCCION EN COLA
                                        if idbrazoActual == idBrazoInstruccion and movimientoAnterior == idComponenteInstruccion:
                                            movAnteiriorEnsamble = copy.deepcopy(movimientoAnterior)
                                            ensamblando = 1
                                            movimiento = Movimiento("EN", i)
                                            listaMovimiento.insertar(movimiento)
                                            colaANTERIORencolar.encolar(movimiento.estadoMovimiento)
                                            contEnsamble += 1
                                        # SE QUEDA CON ESTADO ESPERA
                                        else:
                                            movimiento = Movimiento("s", i)
                                            listaMovimiento.insertar(movimiento)
                                            colaANTERIORencolar.encolar(movimiento.estadoMovimiento)
                                    # SI ESTADO ES UN COMPONENTE Y EN NO ESTA EN COLA A ENSAMBLAR-----
                                    else:
                                        c = int(movimientoAnterior.replace("C", ""))
                                        cp = int(primComponenteEnsamblar.replace("C", ""))
                                        limCom = int(actualB.brazo.cantComponentes.replace("C", ""))
                                        # AVANZAR BRAZO
                                        if c < cp and c <= limCom:
                                            movimiento = Movimiento("C" + str(c + 1), i)
                                            listaMovimiento.insertar(movimiento)
                                            colaANTERIORencolar.encolar(movimiento.estadoMovimiento)
                                        # RETROCEDER BRAZO
                                        if c > cp and c > 0:
                                            movimiento = Movimiento("C" + str(c - 1), i)
                                            listaMovimiento.insertar(movimiento)
                                            colaANTERIORencolar.encolar(movimiento.estadoMovimiento)
                            # SI SE ESTA ENSAMBLANDO********************************************************************
                            else:
                                # SI ESTADO ES NADA---------------------------------------------
                                if movimientoAnterior == "--":
                                    movimiento = Movimiento("--", i)
                                    listaMovimiento.insertar(movimiento)
                                    colaANTERIORencolar.encolar(movimiento.estadoMovimiento)
                                # SI ESTADO ES REPOSO------------------------------------------r
                                if movimientoAnterior == "r":
                                    movimiento = Movimiento("r", i)
                                    listaMovimiento.insertar(movimiento)
                                    colaANTERIORencolar.encolar(movimiento.estadoMovimiento)
                                # SI ESTADO ES ESPERA------------------------------------------s
                                if movimientoAnterior == "s":
                                    movimiento = Movimiento("s", i)
                                    listaMovimiento.insertar(movimiento)
                                    colaANTERIORencolar.encolar(movimiento.estadoMovimiento)
                                # ES ESTADO ES ENSAMBLE----------------------------------------EN
                                if movimientoAnterior == "EN":
                                    tiempoEnsamblaje = actualB.brazo.tiempoEnsamblaje
                                    # SI NO HA LLEGADO AL TIEMPO DE ENSAMBLAJE
                                    if contEnsamble < tiempoEnsamblaje:
                                        movimiento = Movimiento("EN", i)
                                        listaMovimiento.insertar(movimiento)
                                        colaANTERIORencolar.encolar(movimiento.estadoMovimiento)
                                        contEnsamble += 1
                                    # SI YA LLEGO AL TIEMPO DE ENSAMBLAJE
                                    else:
                                        # SI AUN HAY COMPONENTES EN LA COLA DE COMPONENTES A ENSAMBLAR
                                        ensamblando = 0
                                        contEnsamble = 0
                                        # ELIMINA LA INSTRUCCION EN LA COLA INSTRUCCIONES
                                        instru = colaInstruccionesC.desencolar()
                                        colaINSTRUCCIONES.cambiarEstadoInstruccion(instru)
                                        actualB.brazo.colaComponentesEnsamblar.desencolar()
                                        if actualB.brazo.colaComponentesEnsamblar.devolverTam() == 0:
                                            movimiento = Movimiento("r", i)
                                            listaMovimiento.insertar(movimiento)
                                            colaANTERIORencolar.encolar(movimiento.estadoMovimiento)
                                        # SI YA NO HAY COMPONENTES EN LA COLA DE COMPONENTES A ENSAMBLAR
                                        else:
                                            primComponenteEnsamblar = actualB.brazo.colaComponentesEnsamblar.retornarPrimero()
                                            c = int(movAnteiriorEnsamble.replace("C", ""))
                                            cp = int(primComponenteEnsamblar.replace("C", ""))
                                            limCom = int(actualB.brazo.cantComponentes.replace("C", ""))
                                            # AVANZAR BRAZO
                                            if c < cp and c <= limCom:
                                                movimiento = Movimiento("C" + str(c + 1), i)
                                                listaMovimiento.insertar(movimiento)
                                                colaANTERIORencolar.encolar(movimiento.estadoMovimiento)
                                            # RETROCEDER BRAZO
                                            if c > cp and c > 0:
                                                movimiento = Movimiento("C" + str(c - 1), i)
                                                listaMovimiento.insertar(movimiento)
                                                colaANTERIORencolar.encolar(movimiento.estadoMovimiento)
                                # SI ESTADO ES UN COMPONENTE Y EN COLA A ENSAMBLAR--------------
                                if "C" in movimientoAnterior:
                                    if movimientoAnterior == primComponenteEnsamblar:
                                        idBrazoInstruccion = primInstruccion.idBrazo
                                        idComponenteInstruccion = primInstruccion.componente
                                        idbrazoActual = actualB.brazo.idBrazo
                                        # VERIFICA SI EL COMPONENETE Y BRAZO SON LOS DE LA PRIMERA INSTRUCCION EN COLA
                                        if idbrazoActual == idBrazoInstruccion and movimientoAnterior == idComponenteInstruccion:
                                            movAnteiriorEnsamble = copy.deepcopy(movimientoAnterior)
                                            ensamblando = 1
                                            movimiento = Movimiento("EN", i)
                                            listaMovimiento.insertar(movimiento)
                                            colaANTERIORencolar.encolar(movimiento.estadoMovimiento)
                                            contEnsamble += 1
                                        # SE QUEDA CON ESTADO ESPERA
                                        else:
                                            movimiento = Movimiento("s", i)
                                            listaMovimiento.insertar(movimiento)
                                            colaANTERIORencolar.encolar(movimiento.estadoMovimiento)
                                    # SI ESTADO ES UN COMPONENTE Y EN NO ESTA EN COLA A ENSAMBLAR-----
                                    else:
                                        c = int(movimientoAnterior.replace("C", ""))
                                        cp = int(primComponenteEnsamblar.replace("C", ""))
                                        limCom = int(actualB.brazo.cantComponentes.replace("C", ""))
                                        # AVANZAR BRAZO
                                        if c < cp and c <= limCom:
                                            movimiento = Movimiento("C" + str(c + 1), i)
                                            listaMovimiento.insertar(movimiento)
                                            colaANTERIORencolar.encolar(movimiento.estadoMovimiento)
                                        # RETROCEDER BRAZO
                                        if c > cp and c > 0:
                                            movimiento = Movimiento("C" + str(c - 1), i)
                                            listaMovimiento.insertar(movimiento)
                                            colaANTERIORencolar.encolar(movimiento.estadoMovimiento)
                        actualB = actualB.siguiente
                    # ASIGNACION DE COLA A COLA
                    colaANTERIORdesencolar = copy.deepcopy(colaANTERIORencolar)
                print(i - 1)
                actual.Simulacion.estado = "listo"
                actual.Simulacion.tiempoTotal = i - 1
            actual = actual.siguiente

    def generarXMLsalida(self):
        salidaSimulacion = ET.Element('SalidaSimulacion')
        self.crearArchivoHTML()
        actual = self.listaSimulaciones.primero
        while actual is not None:
            if actual.Simulacion.estado == "listo":
                nombre = actual.Simulacion.Nombre
                linea0 = "Nombre Simulacion:" + nombre
                self.escribirLineaHTML(linea0)
                listabrazos = actual.Simulacion.ListaBrazos
                ProductoE = actual.Simulacion.Producto
                nombreSalida = ET.SubElement(salidaSimulacion, "Nombre")
                nombreArchivoSalida = nombre
                nombreSalida.text = nombreArchivoSalida
                listaProductos = ET.SubElement(salidaSimulacion, 'ListadoProductos')
                # PRODUCTO
                producto = ET.SubElement(listaProductos, 'Producto')
                nombreP = ET.SubElement(producto, 'Nombre')
                nombreP.text = ProductoE.nombre
                linea1 = "Nombre Simulacion:" + ProductoE.nombre
                self.escribirLineaHTML(linea1)
                tiempoTotal = ET.SubElement(producto, 'TiempoTotal')
                tieTot = actual.Simulacion.tiempoTotal
                tiempoTotal.text = str(tieTot)
                linea2 = "TiempoTotal:" + str(tieTot)
                self.escribirLineaHTML(linea2)
                elaboracionOptima = ET.SubElement(producto, 'ElaboracionOptima')
                j = 1
                while j <= tieTot:
                    # POR CADA TIEMPO, POR CADA SEGUNDO
                    tiempo = ET.SubElement(elaboracionOptima, 'Tiempo')
                    tiempo.set('NoSegundo', str(j))
                    actualB = listabrazos.primero
                    linea3 = "segundo:" + str(j)
                    while actualB is not None:
                        listaMov = actualB.brazo.listaMovimientos
                        mov = listaMov.buscarPorSegundo(j)
                        # POR CADA LINEA_ENSAMBLAJE
                        lineaEnsamblaje = ET.SubElement(tiempo, 'LineaEnsamblaje')
                        lineaEnsamblaje.set('NoLinea', str(actualB.brazo.idBrazo))
                        lineaEnsamblaje.text = mov.estadoMovimiento
                        linea4 = linea3 + " Linea:" + str(actualB.brazo.idBrazo)+ " Movimiento: "+ mov.estadoMovimiento
                        self.escribirLineaHTML(linea2)
                        actualB = actualB.siguiente
                    j += 1
            actual = actual.siguiente

        datos = ET.tostring(salidaSimulacion)
        datos2 = minidom.parseString(datos)
        texto = datos2.toprettyxml(indent='\t', encoding="'utf-8'")
        # texto2 = texto.decode('utf-8')
        archivoXML = open("ArchivoXML_Salida" + '.xml', 'wb')
        archivoXML.write(texto)
        archivoXML.close()
        print("Archivo Creado Exitosamente!!!")

    def mostrarDocumentacion(self):
        ruta = str("C:\\Users\\Maria\\Documents\\GitHub\\IPC2_Proyecto1_201602659_Jun\\Ensayo-Proyecto2-IPC2.pdf")
        webbrowser.open_new(ruta)

    def mostrarReporteHTML(self):
        # ---------------------------------------------------------
        # ESTA LINEA SERÁ ELIMINADA Y  SERÁ CONVERTIDA EN PARAMETRO
        # nombre = "ReporteHTML"
        # # ---------------------------------------------------------
        # self.crearArchivoHTML(nombre)
        # self.escribirLineaHTML(nombre)
        webbrowser.open_new_tab("C:\\Users\\Maria\\Desktop\\" + "ReporteHTML" + ".html")

    def crearArchivoHTML(self):
        archivo = open("C:\\Users\\Maria\\Desktop\\" + "ReporteHTML" + ".html", "w")
        archivo.close()

    def escribirLineaHTML(self, linea):
        lineaInicial = """<html>
        <br><br><center><p>Simulación Máquina</p></center><br><br>
        <h1><center>Tabla de Ensamblaje</center></h1>
        <br>"""
        # ---------------------------------------------------------
        # ESTA LINEA SERÁ ELIMINADA Y  SERÁ CONVERTIDA EN PARAMETRO
        # ---------------------------------------------------------
        self.cadenaEscritura += linea
        lineafinal = """</html>"""
        unificado = lineaInicial + self.cadenaEscritura + lineafinal
        archivo = open("C:\\Users\\Maria\\Desktop\\" + "ReporteHTML" + ".html", "a")
        archivo.write(unificado)
        archivo.close()
