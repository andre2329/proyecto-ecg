
import scipy.signal

def procesartxt(file_name,frecuencia):
    """
    Esta función devuelve un arreglo con los datos extraidos del archivo de texto file_name

    Ejemplo:

        resultado = procesar("archivo.txt",500)
    
    
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
    return raw,list(filtrado)

def frecpromedio(senal,frecuencia):
    #------------Calcular la frecuencia cardiaca promedio (2 puntos)-------------
    
    umbral = max(senal)*0.9
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
    posR = []
    for i in range(len(inicios)):
        segmento = senal[inicios[i]:finales[i]]
        maximo = max(segmento)
        posR.append(segmento.index(maximo)+inicios[i])

    ciclos = len(posR)-1
    difmuestras = posR[-1]-posR[0]
    tentreextremos = difmuestras/frecuencia

    FreqCard = 60*ciclos/tentreextremos

    return FreqCard,posR
    
#---------Las frecuencias cardiacas instantáneas (2 puntos)-----------------#
def frecsins(posicionesR,frecuencia):
    disentreRs=[]
    for i in range(1,len(posicionesR)):
        disentreRs.append(posicionesR[i]-posicionesR[i-1])

    FreqsIns = []
    for i in disentreRs:
        t = i/frecuencia
        FreqsIns.append(60/t)
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
    senal = list(senal)
    rangovoltaje = vmax-vmin
    voltajeporbit = rangovoltaje/(2**bits)
    amplitudes = []
    posicionesQS = []
    minimoatras = 0
    minimoadelante = 0
    for pos in (posicionesR):
        desplazamiento = int(0.150*frecuencia)
        segmentoatras = senal[pos-desplazamiento:pos][:]
        segmentoatras.reverse()
        segmentoadelante = senal[pos:pos+desplazamiento]
        minimoatras = min(segmentoatras)
        minimoadelante = min(segmentoadelante)
        mingeneral = min(minimoatras,minimoadelante)
        amplitudes.append(int(senal[pos]-mingeneral)*voltajeporbit/ganancia)
        posQ = segmentoatras.index(minimoatras)
        posS = segmentoadelante.index(minimoadelante)
        posicionesQS.append([posQ,posS])

    return amplitudes,posicionesQS

def duracionQRS(posicionesQS,frecuencia):
    duraciones = []
    for pos in posicionesQS:
        duraciones.append(((pos[1]+pos[0])/frecuencia))
    return duraciones


import tkinter as tk
from tkinter import ttk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg,NavigationToolbar2Tk
from tkinter import filedialog
import matplotlib.pyplot as plt

class App:
    def __init__(self,master):
        self.master = master
        self.frecMuestreo = tk.IntVar()
        self.voltajemax = tk.DoubleVar()
        self.voltajemin = tk.DoubleVar()
        self.ganancia = tk.DoubleVar()
        self.bits = tk.IntVar()
        self.archivo = tk.StringVar()
        self.ondas = []
        self.senal_raw = []
        self.senal_fil= []


     #------------valores asignados personales------------
        self.frecMuestreo.set(500)
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
        self.entFreq = tk.Entry(lblfreq,textvariable=self.frecMuestreo,width=4)
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
        lblfreqprom = ttk.Label(lblresumen,text="Frecuencia Cardiaca promedio:",width=40)
        self.freqprom = ttk.Label(lblresumen,text=" ", width=40)
        lblfreqins = ttk.Label(lblresumen,text="Frecuencias Cardiacas instantaneas:",width=40)
        self.freqins = ttk.Label(lblresumen,text=" ",width=40)
        lblritmo = ttk.Label(lblresumen,text="Ritmo y diferencias:",width=40)
        self.diferencias = ttk.Label(lblresumen,text=" ",width=40)
        self.ritmo = ttk.Label(lblresumen,text=" ",width=40)
        lblamplitud = ttk.Label(lblresumen,text="Amplitud del complejo QRS:",width=40)
        self.ampqrs = ttk.Label(lblresumen,text=" ",width=40)
        lblduracion = ttk.Label(lblresumen,text="Duracion del complejo QRS:",width=40)
        self.duracion = ttk.Label(lblresumen,text=" ",width=40)

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
        self.fig, self.ax = plt.subplots(figsize=(12,8))
        self.fig.set_facecolor("#F0F0F0")
        self.graf = FigureCanvasTkAgg(self.fig,master=frmgraf)
        self.graf.get_tk_widget().pack()
        self.ax.tick_params(axis='x',labelsize=8)
        self.ax.set_xlabel("Muestras")
        self.ax.set_ylabel("Amplitud(mV)")
        self.ax.grid(True)
        self.fig.tight_layout()
        
        frmgraf.grid(row=0,column=0, padx=5,pady=5)
        #------------------------- bind ------------------------------
        self.cbondas.bind("<<ComboboxSelected>>",self.graficar)

    def select(self):
        filename = filedialog.askopenfilename()
        self.archivo.set(filename)
    def start(self):
        self.senal_raw, self.senal_fil = procesartxt(self.archivo.get(),self.frecMuestreo.get())
        frec,posR = frecpromedio(self.senal_raw,self.frecMuestreo.get())
        self.freqprom.config(text = f"{int(frec)} BPM")
        frecs = frecsins(posR,self.frecMuestreo.get())
        stringfrec = ""
        for i,val in enumerate(frecs,start=1):
            stringfrec += f"{round(val)} BPM " 
            if (i%5==0):
                stringfrec += "\n"
        self.freqins.config(text=stringfrec)

        diferencias,arritmia = ritmo(frecs)

        stringdif = ""
        for i,dif in enumerate(diferencias,start=1):
            stringdif += f"{dif*1000:2.2f} mS "
            if (i%5==0):
                stringdif += "\n"
        if(frec>=60 and frec<100 ):
            stringdif += "\n\nFrecuencia promedio normal"
        elif(frec>=100):
            stringdif += "\n\nEl paciente presenta Taquicardia"
        else:
            stringdif += "\n\nEl paciente presenta Bradicardia"
        if arritmia:
            stringdif += "\n\nEl paciente presenta arritmia"
        else:
            stringdif += "\n\nEl paciente no presenta arritmia"

        self.diferencias.config(text=stringdif)
        
        amplitudes,posicionesQS = amplitudQRS(self.senal_fil,posR,self.frecMuestreo.get(),self.voltajemax.get(),self.voltajemin.get(),self.bits.get(),self.ganancia.get())

        stringamp = ""
        for i,amp in enumerate(amplitudes,start=1):
            stringamp += f"{amp*1000:.2f} mV "
            if (i%5==0):
                stringamp += "\n"
        self.ampqrs.config(text=stringamp)

        duraciones = duracionQRS(posicionesQS,self.frecMuestreo.get())

        stringduracion = ""
        for i,duracion in enumerate(duraciones,start=1):
            stringduracion += f"{duracion*1000:.2f} mS "
            if (i%5==0):
                stringduracion += "\n"
        self.duracion.config(text=stringduracion)

        self.ondas = []
        strondas = []
        for i,(possR,possqs) in enumerate(zip(posR,posicionesQS)):
            strondas.append(f"Onda {i}")
            self.ondas.append([possR,possqs[0],possqs[1]])
        
        self.cbondas.config(values=strondas)

    def graficar(self,handle):
        self.ax.cla()
        onda = self.cbondas.current()
        info = self.ondas[onda]
        if onda==0:
            limiteizq = 0
            limiteder = int((self.ondas[onda+1][0]+self.ondas[onda][0])/2)
            posiR = info[0]
            posiQ = posiR-info[1]
            posiS = posiR+info[2]
            self.ax.plot(self.senal_raw[:limiteder],color='c',label="Señal ECG")
            self.ax.plot(self.senal_fil[:limiteder],color='r',label="Señal ECG filtrada")
        elif onda==len(self.ondas)-1:
            limiteizq = int((self.ondas[onda][0]+self.ondas[onda-1][0])/2)
            posiR = info[0]-limiteizq
            posiQ = posiR-info[1]
            posiS = posiR+info[2]
            self.ax.plot(self.senal_raw[limiteizq:],color='c',label="Señal ECG")
            self.ax.plot(self.senal_fil[limiteizq:],color='r',label="Señal ECG filtrada") 
           
        else:
            limiteizq = int((self.ondas[onda][0]+self.ondas[onda-1][0])/2)
            limiteder = int((self.ondas[onda+1][0]+self.ondas[onda][0])/2)
            posiR = info[0]-limiteizq
            posiQ = posiR-info[1]
            posiS = posiR+info[2]
            self.ax.plot(self.senal_raw[limiteizq:limiteder],color='c',label="Señal ECG")
            self.ax.plot(self.senal_fil[limiteizq:limiteder],color='r',label="Señal ECG filtrada")
             
        self.ax.legend()   
        self.ax.axvline(x=posiQ,color='k',linestyle="--")
        self.ax.axvline(x=posiS,color='k',linestyle="--")
        self.graf.draw()

root = tk.Tk()
window = App(root)

root.mainloop()


raw,filtrado = procesartxt("senalesECG/Grupo02_b.txt",500)
frecard,posR = frecpromedio(filtrado,500)
frecs = frecsins(posR,500)
dif,arr = ritmo(frecs)
amplitudes,posicionesQS = amplitudQRS(filtrado,posR,500,3,0,10,200)

plt.plot(raw[100:355])
plt.plot(filtrado[100:355])

filtrado[1]

posR



dif


