
import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack


def moda(datos):
    repeticiones = 0

    for i in datos:
        n = datos.count(i)
        if n > repeticiones:
            repeticiones = n

    moda = [] #Arreglo donde se guardara el o los valores de mayor frecuencia 

    for i in datos:
        n = datos.count(i) # Devuelve el número de veces que x aparece enla lista.
        if n == repeticiones and i not in moda:
            moda.append(i)

    if len(moda) != len(datos):
        print ('Moda: ', moda)
    else:
        print ('No hay moda')
    return moda[0]






import scipy.signal

def procesartxt(file_name,frecuencia):
    """
    Esta función devuelve un arreglo con los datos extraidos del archivo de texto file_name

    Ejemplo:

        resultado_filtrado = procesar("archivo.txt",500)
    
    
    """
    raw = []
    with open(file_name,'r') as file:
        for i in file:
            raw.append(int(i[:-1]))
    #---------------------------filtro------------------------------------------
    n = 61
    cutfreq = 30
    a = scipy.signal.firwin(n, cutoff = 2*cutfreq/frecuencia, window = "hamming")
    filtrado = scipy.signal.filtfilt(a,1,raw)
    return raw,filtrado

def frecpromedio(senal,frecuencia):
    #------------Calcular la frecuencia cardiaca promedio (2 puntos)-------------
    umbral = max(senal)*0.8
    auxiliar = []
    for i in senal:
        if(i>umbral):
            auxiliar.append(i)
        else:
            auxiliar.append(0)
    inicios = []
    finales = []
    for i in range(1,len(auxiliar)):
        if(auxiliar[i]-auxiliar[i-1]>200):
            inicios.append(i)
        elif(auxiliar[i]-auxiliar[i-1]<-200):
            finales.append(i)
    picosR = []
    posR = []
    for i in range(len(inicios)):
        segmento = arreglo[inicios[i]:finales[i]]
        maximo = max(segmento)
        picosR.append(maximo)
        posR.append(segmento.index(maximo)+inicios[i])

    ciclos = len(posR)-1
    difmuestras = posR[-1]-posR[0]
    tentreextremos = difmuestras/frecuencia

    FreqCard = 60*ciclos/tentreextremos

    return FreqCard,posR,picosR
    
#---------Las frecuencias cardiacas instantáneas (2 puntos)-----------------#
def frecsins(posicionesR,frecuencia):
    disentreRs=[]
    for i in range(1,len(posicionesR)):
        disentreRs.append(posicionesR[i]-posicionesR[i-1])

    FreqsIns = []
    for i in disentreRs:
        t = i/frecuencia
        FreqsIns.append(60/t)
        tentreR.append(t)
    return FreqsIns

def ritmo(frecuenciasIns):
    """c) El ritmo cardiaco (4 puntos)"""
    tentreR = []
    arritmia = False
    diferencias = []
    for i in frecuenciasIns:
        tentreR.append(60/i)
    for i in range(1,len(tentreR)):
        diferencia = abs(tentreR[i]-tentreR[i-1])
        diferencias.append(diferencia)
        if(diferencia>=0.04):
            arritmia=True
    return diferencias,arritmia

def amplitudQRS(senal,posicionesR,frecuencia,vmax,vmin,bits,ganancia):
    """"d) Las amplitudes de los complejos QRS (5 puntos)
hallando los Q"""
    rangovoltaje = vmax-vmin
    voltajeporbit = rangovoltaje/(2**bits)
    amplitudes = []
    posicionesQS = []
    for pos in (posicionesR):
        segmentoatras = senal[posicionesR-int(0.150*frecuencia)]
        segmentoadelante = senal[posicionesR+int(0.150*frecuencia)]
        minimoatras = min(segmentoatras)
        minimoadelante = min(segmentoadelante)
        mingeneral = min(minimoatras,minimoadelante)
        amplitudes.append(int(senal[pos]-mingeneral)*voltajeporbit/ganancia)
        posQ = pos - segmentoatras.index(minimoatras)
        posS = pos + segmentoadelante.index(minimoadelante)
        posicionesQS.append([posQ,posS])

    return amplitudes,posicionesQS

def duracionQRS(senal,posicionesQS,frecuencias):
    duraciones = []
    for pos in posicionesQS:
        duraciones.append((pos[1]-pos[0])/frecuencia)
    return duraciones

import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from tkinter import filedialog
import matplotlib.pyplot as plt

class App:
    def __init__(self,master):
        self.master = master
        self.frecuencia = tk.IntVar()
        self.voltajemax = tk.DoubleVar()
        self.voltajemin = tk.DoubleVar()
        self.ganancia = tk.DoubleVar()
        self.bits = tk.IntVar()
        self.archivo = tk.StringVar()
        self.ondas = []
        self.senal = []
        

     #------------valores asignados personales------------
        self.frecuencia.set(500)
        self.voltajemax.set(3.3)
        self.voltajemin.set(0)
        self.ganancia.set(200)
        self.bits.set(10)
#----------------------- frm ---------------------------------------
        frm = tk.Frame(self.master,bg="#F0F0F0")
        frm1 = tk.Frame(frm,bg="#F0F0F0")
        frm2 = tk.Frame(frm,bg="#F0F0F0")

        frm.pack(padx=10,pady=10)
        frm1.pack(side=tk.LEFT,anchor=tk.N)
        frm2.pack(side=tk.LEFT,anchor=tk.N)

    #--------------------frm 1 ------------------------#
     #----------------frm seleccion archivo -----------------#
        lblfrm = ttk.LabelFrame(frm1,text="Archivo",labelanchor='n')
        self.btnfile = tk.Button(lblfrm,text="...",command=self.select)
        self.lblfile = tk.Entry(lblfrm,textvariable=self.archivo)

        
        self.btnfile.grid(row=0,column=1)
        self.lblfile.grid(row=0,column=0)
    #----------------frm datos -----------------#
        #---------------- freq -----------------#
        lblfreq = ttk.LabelFrame(frm1,text="Frecuencia de muestreo (Hz)")
        self.entFreq = tk.Entry(lblfreq,textvariable=self.frecuencia,width=4)
        self.entFreq.pack()
        #---------------- bits -----------------#
        lblbits = ttk.LabelFrame(frm1,text="Bits")
        self.entbits = tk.Entry(lblbits,textvariable=self.bits,width=3)
        self.entbits.pack()
        #---------------- voltajes -----------------#
        lblmax = ttk.LabelFrame(frm1,text="Vmax:",labelanchor='n')
        self.entmax = tk.Entry(lblmax,textvariable=self.voltajemax,width=3)
        self.entmax.pack()
        lblmin = ttk.LabelFrame(frm1,text="Vmin:",labelanchor='n')
        self.entmin = tk.Entry(lblmin,textvariable=self.voltajemin,width=3)
        self.entmin.pack()
        #---------------- ganancia -----------------#
        lblgan = ttk.LabelFrame(frm1,text="Ganancia",labelanchor='n')
        self.entgan = tk.Entry(lblgan,textvariable=self.ganancia,width=3)
        self.entgan.pack()
        #---------------- ondas -----------------#
        lblondas = ttk.LabelFrame(frm1,text="Ondas",labelanchor='n')
        self.cbondas = ttk.Combobox(lblondas,values=self.ondas)
        self.cbondas.pack()
        #---------------- boton -----------------#
        self.btnInicio = tk.Button(frm1,text="Inicio",width=12,heigh=3,command=self.start)
        #---------------- resumen -----------------#

        lblresumen = ttk.LabelFrame(frm1,text="Resumen General",labelanchor='n')
        lblfreqprom = ttk.Label(lblresumen,text="Frecuencia Cardiaca promedio:",width=30)
        self.freqprom = ttk.Label(lblresumen,text=" ",width=10)
        lblfreqins = ttk.Label(lblresumen,text="Frecuencias Cardiacas instantaneas:",width=30)
        self.freqins = ttk.Label(lblresumen,text=" ",width=10)
        lblritmo = ttk.Label(lblresumen,text="Ritmo y diferencias:",width=30)
        self.diferencias = ttk.Label(lblresumen,text=" ",width=10)
        self.ritmo = ttk.Label(lblresumen,text=" ",width=10)
        lblamplitud = ttk.Label(lblresumen,text="Amplitud del complejo QRS:",width=30)
        self.ampqrs = ttk.Label(lblresumen,text=" ",width=10)
        lblduracion = ttk.Label(lblresumen,text="Duracion del complejo QRS:",width=30)
        self.duracion = ttk.Label(lblresumen,text=" ",width=10)

        lblfreqprom.grid(row=0,column=0)
        self.freqprom.grid(row=1,column=0)
        lblfreqins.grid(row=2,column=0)
        self.freqins.grid(row=3,column=0)
        lblritmo.grid(row=4,column=0)
        self.diferencias.grid(row=5,column=0)
        self.ritmo.grid(row=6,column=0)
        lblamplitud.grid(row=7,column=0)
        self.ampqrs.grid(row=8,column=0)
        lblduracion.grid(row=9,column=0)
        self.duracion.grid(row=10,column=0)
        #---------------grid Frm1-----------------------------
        lblfrm.grid(row=0,column=0,columnspan=3)
        lblfreq.grid(row=1,column=0,columnspan=2)
        lblbits.grid(row=1,column=2)
        lblmax.grid(row=2,column=0)
        lblmin.grid(row=2,column=1)
        lblgan.grid(row=2,column=2)
        lblondas.grid(row=3,column=0,columnspan=3)
        
        self.btnInicio.grid(row=4,column=0,columnspan=3)
        lblresumen.grid(row=5,column=0,columnspan=3)
        
    #----------------frm2 -----------------#
        #---------------- Grafico -----------------#
        plt.style.use('ggplot')
        frmgraf = ttk.LabelFrame(frm2,text="ECG",labelanchor='n')
        self.fig, self.ax = plt.subplots(figsize=(9,5))
        self.fig.set_facecolor("#F0F0F0")
        self.graf = FigureCanvasTkAgg(self.fig,master=frmgraf)
        self.graf.get_tk_widget().pack()
        self.ax.tick_params(axis='x',labelsize=8)
        self.ax.set_xlabel("Muestras")
        self.ax.set_ylabel("Amplitud(mV)")
        self.ax.grid(True)
        self.fig.tight_layout()
        
        #---------------- Resumen onda actual -----------------#

        frmonda = ttk.LabelFrame(frm2,text="Resumen onda actual",labelanchor='n',width=50)
        self.lblamplitud = ttk.Label(frmonda,text="AmplitudQRS")

        self.lblamplitud.grid(row=0,column=0)

        frmgraf.grid(row=0,column=0,columnspan=2, padx=5,pady=5)
        frmonda.grid(row=1,column=0,columnspan=2, padx=5,pady=5)


    def select(self):
        filename = filedialog.askopenfilename()
        self.archivo.set(filename)
    def start(self):
        self.senal = procesartxt(self.archivo.get(),self.frecuencia.get())

        pass

root = tk.Tk()
window = App(root)

root.mainloop()


plt.plot(arreglo)


import scipy.signal
n = 61
cutfreq = 30
a = scipy.signal.firwin(n, cutoff = 2*cutfreq/frecuencia, window = "hamming")


filtrado = scipy.signal.filtfilt(a,1,arreglo)






plt.plot(filtrado)

tam = len(filtrado)
plt.plot(arreglo[:1000])
plt.plot(filtrado[:1000])



len(filtrado)


fig,ax = plt.subplots(figsize=(9,5))
ax.clear()
ax.set_title("Grafica ECG")
ax.set_xlabel("Muestras")
ax.set_ylabel("Amplitud(mV)")
ax.plot(arreglo)
ax.grid(True)


