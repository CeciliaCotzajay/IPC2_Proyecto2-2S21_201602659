from tkinter import *
from tkinter import filedialog, messagebox

# from MetodosMaquina import MetodosMaquina

raizPre = Tk()
# M = MetodosMaquina()


# **********************************************************************************************************************
# ***************************************** MÉTODOS AUXILIARES *********************************************************
# **********************************************************************************************************************


def verDocumentacion():
    print("docu")
    # M.mostrarDocumentacion()


def abrir_cargarArchivo():
    # try:
    rutaFichero = filedialog.askopenfilename(title="Abrir Archivo", initialdir="C:\\Users\\Maria\\Desktop",
                                             filetypes=(
                                                 ("Ficheros XML", "*.xml"), ("Todos los ficheros", "*.*")))
    if rutaFichero is None:
        messagebox.showinfo("Abrir Archivo", "No ha Elegido ningún Archivo...")
    else:
        print(rutaFichero)
        # M.cargarArchivo(rutaFichero)


def resetear():
    messagebox.showwarning("Abrir Archivo", "No ha Elegido ningún Archivo...")


# **********************************************************************************************************************
# ***************************************** INTERFAZ GRÁFICA ***********************************************************
# **********************************************************************************************************************

def abrirVentanaPrincipal():
    raizPre.withdraw()
    raiz = Toplevel()
    raiz.title("PROYECTO 1 - IPC2!")
    raiz.iconbitmap("img/i.ico")
    raiz.config(bg="#F85409")  # #1A5276
    raiz.config(bd=25, width=800, height=615)
    raiz.config(relief="sunken")
    raiz.config(cursor="circle")
    # ----------------------------------------------------------------------------------------------------------------------
    frameP = Frame(raiz)
    frameP.pack()
    frameP.config(width="800", height="615")
    frameP.config(bg="black")
    frameP.config(bd=4)
    frameP.config(cursor="hand2")
    # ----------------------------------------------------------------------------------------------------------------------
    barraMenu = Menu(raiz)
    raiz.config(menu=barraMenu)

    archivoMenu = Menu(barraMenu, tearoff=0)
    archivoMenu.add_command(label="- Configurar Máquina..")
    archivoMenu.add_command(label="- Cargar Coponentes...", command=abrir_cargarArchivo)
    archivoMenu.add_separator()
    archivoMenu.add_command(label="-Salir del Juego", command=raiz.destroy)
    archivoMenu.config(fg="#00FF00", bg="#454545", font=("Comic Sans MS", 10))

    peticionesMenu = Menu(barraMenu, tearoff=0)
    peticionesMenu.add_command(label="- Ver HTML..")
    peticionesMenu.add_command(label="- Ver Graphviz..")
    peticionesMenu.config(fg="#00FF00", bg="#454545", font=("Comic Sans MS", 10))

    ayudaMenu = Menu(barraMenu, tearoff=0)
    ayudaMenu.add_command(label="- Documentación", command=verDocumentacion)
    ayudaMenu.add_command(label="- Acerca de...", command=abrirVentanaAcercaDe)
    ayudaMenu.config(fg="#00FF00", bg="#454545", font=("Comic Sans MS", 10))

    barraMenu.add_cascade(label="Archivo", menu=archivoMenu)
    barraMenu.add_cascade(label="Reportes", menu=peticionesMenu)
    barraMenu.add_cascade(label="Ayuda", menu=ayudaMenu)
    barraMenu.config(fg="#00FF00", bg="#454545", font=("Comic Sans MS", 10))
    # ------------------------------------------------------------------------------------------------------------------
    # DATOS DE LOS JUGADORES
    # ------------------------------------------------------------------------------------------------------------------
    botonMostrarDatos = Button(raiz, text="Refrescar Tablero")
    botonMostrarDatos.config(bg="#82E0AA", font=("Comic Sans MS", 10))
    botonMostrarDatos.place(x=50, y=40)
    botonMostrarDatos.config(cursor="hand2")
    # ------------------------------------------------------------------------------------------------------------------
    # ------------------------------------------------------------------------------------------------------------------
    raiz.mainloop()
    raizPre.destroy()


def abrirVentanaAcercaDe():
    raizAcer = Toplevel()
    raizAcer.title("Bienvenidos!")
    raizAcer.iconbitmap("img/i.ico")
    raizAcer.config(bg="purple")  # FED509
    raizAcer.config(bd=25)
    raizAcer.config(relief="groove")
    raizAcer.config(cursor="circle")
    # ----------------------------------------------------------------------------------------------------------------------
    FrameAD = Frame(raizAcer)
    FrameAD.pack()
    FrameAD.config(width="610", height="350")
    FrameAD.config(bg="black")
    FrameAD.config(bd=15)
    FrameAD.config(relief="sunken")
    FrameAD.config(cursor="dot")
    # ----------------------------------------------------------------------------------------------------------------------
    fondo01 = PhotoImage(file="img/i0.png")
    fondo02 = fondo01.subsample(2)
    # ----------------------------------------------------------------------------------------------------------------------
    label1 = Label(FrameAD, image=fondo02)
    label1.place(x=30, y=20)
    Label(FrameAD, text="Introducción a la Programación y Computación 2", justify="center", bg="#D2B4DE", fg="Purple",
          font=("Comic Sans MS", 10)).place(x=275, y=70)
    Label(FrameAD, text="Sección E", bg="#82E0AA", font=("Comic Sans MS", 11)).place(x=380, y=125)
    Label(FrameAD, text="María Cecilia Cotzajay López", fg="Purple", bg="#D2B4DE", font=("Comic Sans MS", 10)).place(
        x=330, y=175)
    Label(FrameAD, text="201602659", bg="#82E0AA", font=("Comic Sans MS", 11)).place(x=370, y=230)
    # ----------------------------------------------------------------------------------------------------------------------
    botonAcercaDe = Button(raizAcer, text="Cerrar", command=raizAcer.destroy)
    botonAcercaDe.config(fg="#00FF00", bg="#454545", font=("Comic Sans MS", 10))
    botonAcercaDe.place(x=250, y=300)
    botonAcercaDe.config(cursor="hand2")
    #
    # ----------------------------------------------------------------------------------------------------------------------
    raizAcer.mainloop()


raizPre.title("PROYECTO 2 - IPC2!")
raizPre.iconbitmap("img/i.ico")
raizPre.config(bg="#F85409")  # #FED509
raizPre.config(bd=25)
raizPre.config(relief="groove")
raizPre.config(cursor="circle")
# ----------------------------------------------------------------------------------------------------------------------
Frame1 = Frame(raizPre)
Frame1.pack()
Frame1.config(width="625", height="350")
Frame1.config(bg="black")
Frame1.config(bd=15)
Frame1.config(relief="sunken")
Frame1.config(cursor="dot")
# ----------------------------------------------------------------------------------------------------------------------
fondo = PhotoImage(file="img/ip.png")  # SÓLO ACEPTA PNG y GIF, CON JPG DA ERROR
fondo0 = fondo.subsample(2)
fondo1 = PhotoImage(file="img/i2.png")  # SÓLO ACEPTA PNG y GIF, CON JPG DA ERROR
fondo2 = fondo1.subsample(4)
fondo3 = PhotoImage(file="img/i0.png")  # SÓLO ACEPTA PNG y GIF, CON JPG DA ERROR
fondo4 = fondo3.subsample(4)
# ----------------------------------------------------------------------------------------------------------------------
label11 = Label(Frame1, image=fondo2)
label11.place(x=30, y=70)
label0 = Label(Frame1, image=fondo0)
label0.place(x=225, y=30)
label22 = Label(Frame1, image=fondo4)
label22.place(x=230, y=160)
Label(Frame1, text="IPC - 2", fg="Purple", bg="#D2B4DE", font=("Comic Sans MS", 20)).place(x=440, y=55)
Label(Frame1, text="Proyecto 2 ", bg="#82E0AA", font=("Comic Sans MS", 12)).place(x=443, y=110)
Label(Frame1, text="SEP-2021", bg="#D2B4DE", font=("Comic Sans MS", 12)).place(x=455, y=160)
# ----------------------------------------------------------------------------------------------------------------------
botonIniciar = Button(raizPre, text="Iniciar!", command=abrirVentanaPrincipal)
botonIniciar.config(fg="#00FF00", bg="#454545", font=("Comic Sans MS", 10))
botonIniciar.place(x=480, y=260)
botonIniciar.config(cursor="hand2")
# ----------------------------------------------------------------------------------------------------------------------
raizPre.mainloop()
