"""
Estimados alumnos. 

En los archivos adjuntos encontrarán en el Excel la señal que le corresponde con los datos para poder procesarla. En el archivo .rar encontrarán las muestras con las señales de ECG. 

Deben realizar un algoritmo en Python o en Visual C++. El algoritmo deberá calcular lo siguiente:

a) Calcular la frecuencia cardiaca promedio (2 puntos)

b) Las frecuencias cardiacas instantáneas (2 puntos)

c) El ritmo cardiaco (4 puntos)

d) Las amplitudes de los complejos QRS (5 puntos)

e) La duración de los complejos QRS (7 puntos)

Deberán subir el algoritmo creado y un audio de no más de 3 minutos que explique como implementaron su estrategia de procesamiento de la señal de ECG.

Tiene hasta el viernes 29 de mayo para subir la solución a las 15:00 horas.


EL72	201726246	 Rodriguez Canahuire, Juan Andres	Grupo02_b	500Hz	200	3.3V	0V	10


"""
#%%
arreglo = []
with open("/Users/juan/Desktop/ECG/Grupo02_b.txt",'r') as file:
    for i in file:
        arreglo.append(i)

# %%
new = []
for i in arreglo:
    new.append(int(i[:-1]))

# %%
print(new)

# %%
import matplotlib.pyplot as plt

plt.plot(new[0:500])
plt.show()

# %%
max(new)

# %%
och = max(new)*0.8
aux = []
for i in new:
    if i>och:
        aux.append(i)
    else:
        aux.append(0)
inicios = []
finales = []
for i in range(1,len(aux)):
    if(aux[i]-aux[i-1]>200):
        inicios.append(i)
    if(aux[i]-aux[i-1]<-200):
        finales.append(i)


# %%
print(inicios)
print(finales)

# %%
maxi = []
posmax = []
for i in range(len(inicios)):
    maxi.append(max(aux[inicios[i]:finales[i]]))
    posmax.append(aux.index(maxi[i]))
print(maxi)
print(posmax)
# %%
print(new[202:697].index(min(new[202:697])))
print(new[new[202:697].index(min(new[202:697]))+202-1])
print(new[new[202:697].index(min(new[202:697]))+202])
print(new[new[202:697].index(min(new[202:697]))+202+1])
# %%
print(inicios)
print(finales)
plt.plot(new[posmax[0]:posmax[1]])
plt.show()

# %%
didi = new[posmax[0]:posmax[1]]
promedios = []
for i in range(1,len(new[posmax[0]:posmax[1]])):
    print(didi[i],didi[i-1],(didi[i]+didi[i-1])/2)
    promedios.append((didi[i]+didi[i-1])/2)

plt.plot(promedios)
# %%

promedios2 = []
for i in range(1,len(promedios)):
    promedios2.append((promedios[i]+promedios[i-1])/2)

plt.plot(promedios)


# %%
from __future__ import division
import numpy as np
import matplotlib.pyplot as plt

data = np.asarray(new)
ps = np.abs(np.fft.fft(data))**2

time_step = 1/500
freqs = np.fft.fftfreq(data.size, time_step)
idx = np.argsort(freqs)

plt.plot(freqs,20*np.log(ps))
ps

# %%
print(ps)

# %%
from scipy import signal
fs = 500.0  # Sample frequency (Hz)
f0 = 60.0  # Frequency to be removed from signal (Hz)
Q = 30.0  # Quality factor
w0 = f0 / (fs / 2 )  # Normalized Frequency
b, a = signal.iirnotch( w0, Q )
# Look at frequency response
w, h = signal.freqz( b, a )
freq = w * fs / ( 2 * np.pi )
x=[]
for i in range(len(h)):
    x.append(h[i]*ps[i])
plt.plot( freq, 20*np.log10( abs(np.asarray(x)) ) )




# %%
resultado = np.fft.ifft(x)

plt.plot(resultado[0:150])

# %%
import numpy as np
import pylab as pl
rate = 500.0
t = np.asarray(new)
x = np.sin(2*np.pi*4*t) + np.sin(2*np.pi*7*t) + np.random.randn(len(t))*0.2
p = 20*np.log10(np.abs(np.fft.rfft(x)))
f = np.linspace(0, rate/2, len(p))
plt.plot(f, p)

# %%

import numpy as np
import matplotlib.pyplot as plt
import scipy.fftpack

# sample spacing
T=1/500.0 
N=len(new)
y=np.asarray(new)
yf = scipy.fftpack.fft(y)
xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
fig, ax = plt.subplots()

ax.plot(xf[1:], 2.0/N * np.abs(yf[:N//2])[1:])
plt.show()
yaux=yf[:N//2]
xnew=[]
ynew=[]
for i in (range(len(xf))):

    if xf[i]>59.9 and xf[i]<60.1:
        ynew.append(0)
    else:
        ynew.append(yaux[i])
    xnew.append(xf[i])

# %%
plt.plot(xnew[1:],np.abs(ynew[1:]))

xnew[ynew.index(max(ynew[1:]))]

yew = scipy.fftpack.ifft(ynew)
# %%
plt.plot(yew[:500])
output_signal = scipy.signal.filtfilt(b, a, y)

# %%
plt.plot(output_signal[:250])
# %%
fs = 200.0  # Sample frequency (Hz)
f0 = 60.0  # Frequency to be removed from signal (Hz)
Q = 30.0  # Quality factor
w0 = f0 / (fs / 2 )  # Normalized Frequency
b, a = signal.iirnotch( w0, Q )
# Look at frequency response
w, h = signal.freqz( b, a )
freq = w * fs / ( 2 * np.pi )
plt.plot( freq, 20*np.log10( abs(output_signal) ) )



# %%

T=1/500.0 
N=len(new)
y=np.asarray(new)
yf = scipy.fftpack.fft(output_signal)
xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
fig, ax = plt.subplots()

ax.plot(xf[1:], 2.0/N * np.abs(yf[:N//2])[1:])
plt.show()
yaux=yf[:N//2]
xnew=[]
ynew=[]
for i in (range(len(xf))):

    if xf[i]>59.9 and xf[i]<60.1:
        ynew.append(0)
    else:
        ynew.append(yaux[i])
    xnew.append(xf[i])
# %%
plt.plot(arreglo[:1000])

# %%
T=1/500.0 
N=len(new)
y=np.asarray(new)
yf = scipy.fftpack.fft(new)
xf = np.linspace(0.0, 1.0/(2.0*T), N/2)
fig, ax = plt.subplots()

ax.plot(xf[1:], 2.0/N * np.abs(yf[:N//2])[1:])
plt.show()
yaux=yf[:N//2]
xnew=[]
ynew=[]
for i in (range(len(xf))):

    if xf[i]>55 and xf[i]<65:
        ynew.append(0)
    else:
        ynew.append(yaux[i])
    xnew.append(xf[i])

# %%
plt.plot(xnew[1:], 2.0/N * np.abs(ynew[:N//2])[1:])

# %%
result = scipy.fftpack.ifft(ynew)

plt.plot(result[250:750])

# %%
