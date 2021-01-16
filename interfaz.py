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
        self.bits = tk.IntVar()
        self.ondas = []
        self.archivo = tk.StringVar()

        frm = tk.Frame(self.master)
        frm1 = tk.Frame(frm)
        frm2 = tk.Frame(frm)

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
        lblfreq = ttk.LabelFrame(frm1,text="Frecuencia de muestreo")
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
        #---------------- ondas -----------------#
        lblondas = ttk.LabelFrame(frm1,text="Ondas",labelanchor='n')
        self.cbondas = ttk.Combobox(lblondas,values=self.ondas)
        self.cbondas.pack()
        #---------------- boton -----------------#
        self.btnInicio = tk.Button(frm1,text="Inicio",width=12,heigh=3)
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
        lblfrm.grid(row=0,column=0,columnspan=2)
        lblfreq.grid(row=1,column=0)
        lblbits.grid(row=1,column=1)
        lblmax.grid(row=2,column=0)
        lblmin.grid(row=2,column=1)
        lblondas.grid(row=3,column=0,columnspan=2)
        self.btnInicio.grid(row=4,column=0,columnspan=2)
        lblresumen.grid(row=5,column=0,columnspan=2)
        
    #----------------frm2 -----------------#
        #---------------- Grafico -----------------#
        frmgraf = tk.LabelFrame(frm2,text="ECG")
        self.fig, self.ax = plt.subplots(figsize=(9,5))
        self.fig.set_facecolor("#F0F0F0")
        self.graf = FigureCanvasTkAgg(self.fig,master=frmgraf)
        self.graf.get_tk_widget().pack()
        self.ax.set_xticks([])
        self.ax.set_yticks([])
        self.ax.set_xlabel("Dates")
        self.ax.set_ylabel("Num. People")
        self.ax.tick_params(axis='x',labelsize=8)
        self.fig.tight_layout()
        
        frmgraf.grid(row=0,column=0,columnspan=2, padx=5,pady=5)


    def select(self):
        filename = filedialog.askopenfilename()
        self.archivo.set(filename)


root = tk.Tk()
window = App(root)

root.mainloop()
