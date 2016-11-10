#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
from random import randint
import numpy as np
import sys

from flask import Flask, url_for, jsonify, request
from flask.ext.cors import CORS, cross_origin
app = Flask(__name__)


"""
http://www.scielo.org.mx/scielo.php?script=sci_arttext&pid=S0187-75852006000300004
Resultados: La edad de los pacientes estudiados fue 51 ± 16 años. La tuberculosis pulmonar (29.5%) y neumonía intersticial (14.8%) fueron los diagnósticos más frecuentes. La diferencia media ± desviación estándar de la diferencia (y la media observada ± desviación estándar) de los signos vitales adquiridos por los tres grupos de enfermeras fueron: frecuencia cardiaca, 0.148 ± 6.71 (83.29 ± 10.04); frecuencia respiratoria, 0.197 ± 1.53 (23.69 ± 2.24); temperatura, 0.048 ± 0.204 (36.19 ± 0.33); presión arterial sistémica sistólica, 1.35 ± 6.02 (114.75 ± 10.91) y la presión arterial sistémica diastólica, 0.123 ± 6.12 (71.70 ± 8.25). La magnitud del acuerdo para todos los signos vitales entre los grupos diferenciales de enfermeras (especialistas–generales, generales–auxiliares y especialistas–auxiliares) fueron entre 0.69 y 0.89.

def hilo_temp():
    global temp, contador, pulso, presionSS, presionSD respiracion
    while True:
        # modifica la temperatura cada 5 segundo
        if contador % 5 == 0:
            mu, sigma = 98.2249, 0.733 # media y desvstd
            temp = np.random.normal(mu, sigma)
            temp = (temp - 32) * 5.0/9.0 # fahren a celsius
            temp = round(temp, 2)
        # presion  alto por arriba 120 malo   bajo arriba 80 malo  
        muSS, sigmaSS = 114.75, 10.91 # media y desvstd
            presionSS = np.random.normal(muSS, sigmaSS)
            presionSS = round(pulso)
        muSD, sigmaSD = 71.70, 8.25 # media y desvstd
            presionSD = np.random.normal(muSD, sigmaSD)
            presionSD = round(pulso)
        # respiracion rango normal para un adulto entre 15 a 20 respiraciones por minuto
        muResp, sigmaResp = 23.69, 2.24 # media y desvstd
            respiracion = np.random.normal(muResp, sigmaResp)
            respiracion = round(respiracion) 
        # pulso rango normal para un adulto entre 60 a 100 latidos por minuto
        muPuls, sigmaPuls = 83.29, 10.04 # media y desvstd
            pulso = np.random.normal(muPuls, sigmaPuls)
            pulso = round(pulso)
"""
temp = 0
contador = 0
panic_temp = False


def get_normal_temp():
    mu, sigma = 98.2249, 0.733 # media y desvstd
    temp = np.random.normal(mu, sigma)
    temp = (temp - 32) * 5.0/9.0 # fahren a celsius
    temp = round(temp, 2)
    return temp

def get_panic_temp():
    return 100

def hilo_var():
    global temp, contador, panic_temp
    while True:
        # modifica la temperatura cada 5 segundo
        if contador % 3 == 0:
            if panic_temp:
                temp = get_panic_temp()
            else:
                temp = get_normal_temp() 
        contador += 1
        time.sleep(1)


@app.route('/', methods = ['GET', 'POST'])
@cross_origin() 
def api_root():
    if request.method == 'GET':
        global temp, panic_temp
        res = {'temperatura': temp}
        return jsonify(**res)
    elif request.method == 'POST':
        res = "No se hizo nada"
        panic_var = request.form['panic_var']
        if panic_var == 'temp':
            panic_temp = not panic_temp
            res = "Status de variable temp: " + str(panic_temp) 
        # todo otras variables
        return res


if __name__ == '__main__':
    try:
        t = threading.Thread(target=hilo_var)
        t.start()
        app.run(port=3000)
    except KeyboardInterrupt:
        sys.exit()
