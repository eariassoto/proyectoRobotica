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

# variables del monitor
temp = 0
panic_temp = False
pulso = 0
panic_pulso = False
presionSS = 0
panic_presionSS = False
presionSD = 0
panic_presionSD = False
respiracion = 0
panic_respiracion = False
contador = 0


def get_normal_temp():
	mu, sigma = 98.2249, 0.733 # media y desvstd
	temp = np.random.normal(mu, sigma)
	temp = (temp - 32) * 5.0/9.0 # fahren a celsius
	temp = round(temp, 2)
	return temp

def get_panic_temp():
	return 100

def get_normal_presionSS():
	# presion  alto por arriba 120 malo   bajo arriba 80 malo  
	muSS, sigmaSS = 114.75, 10.91 # media y desvstd
	presionSS = np.random.normal(muSS, sigmaSS)
	presionSS = round(presionSS, 2)
	return presionSS


def get_panic_presionSS():
	return 140


def get_normal_presionSD():
	# presion  alto por arriba 120 malo   bajo arriba 80 malo
	muSD, sigmaSD = 71.70, 8.25 # media y desvstd
	presionSD = np.random.normal(muSD, sigmaSD)
	presionSD = round(presionSD, 2)
	return presionSD


def get_panic_presionSD():
	return 100


def get_normal_respiracion():
	# respiracion rango normal para un adulto entre 15 a 20 respiraciones por minuto
	muResp, sigmaResp = 23.69, 2.24 # media y desvstd
	respiracion = np.random.normal(muResp, sigmaResp)
	respiracion = round(respiracion, 2) 
	return respiracion


def get_panic_respiracion():
	return 30


def get_normal_pulso():
	# pulso rango normal para un adulto entre 60 a 100 latidos por minuto
	muPuls, sigmaPuls = 83.29, 10.04 # media y desvstd
	pulso = np.random.normal(muPuls, sigmaPuls)
	pulso = round(pulso, 2)
	return pulso


def get_panic_pulso():
	return 120


def hilo_var():
	global contador, temp, panic_temp, pulso, panic_pulso, presionSS, panic_presionSS, presionSD, panic_presionSD, respiracion, panic_respiracion 
	while True:
		# modifica la temperatura cada 5 segundo
		if contador % 2 == 0:
			if panic_temp:
				temp = get_panic_temp()
			else:
				temp = get_normal_temp()
				
			if panic_pulso:
				pulso = get_panic_pulso()
			else:
				pulso = get_normal_pulso()
				
			if panic_presionSS:
				presionSS = get_panic_presionSS()
			else:
				presionSS = get_normal_presionSS() 
				
			if panic_presionSD:
				presionSD = get_panic_presionSD()
			else:
				presionSD = get_normal_presionSD()
				
			if panic_respiracion:
				respiracion = get_panic_respiracion()
			else:
				respiracion = get_normal_respiracion() 
		contador += 1
		time.sleep(1)


@app.route('/', methods = ['GET', 'POST'])
@cross_origin() 
def api_root():
	global temp, panic_temp, pulso, panic_pulso, presionSS, panic_presionSS, presionSD, panic_presionSS, respiracion, panic_respiracion
	if request.method == 'GET':		
		res = {'temperatura': temp, 'pulso': pulso, 'presionSS': presionSS, 'presionSD': presionSD, 'respiracion': respiracion}
		return jsonify(**res)
		
	elif request.method == 'POST':
		res = "No se hizo nada"
		panic_var = request.form['panic_var']
		
		if panic_var == 'temp':
			panic_temp = not panic_temp
			res = "Status de variable temp: " + str(panic_temp)
			
		elif panic_var == 'pulso':
			panic_pulso = not panic_pulso
			res = "Status de variable pulso: " + str(panic_pulso)
			
		elif panic_var == 'presionSS':
			panic_presionSS = not panic_presionSS
			res = "Status de variable presionSS: " + str(panic_presionSS)
			
		elif panic_var == 'presionSD':
			panic_presionSD = not panic_presionSD
			res = "Status de variable presionSD: " + str(panic_presionSD)
			
		elif panic_var == 'respiracion':
			panic_respiracion = not panic_respiracion
			res = "Status de variable respiracion: " + str(panic_respiracion)
			
		return res


if __name__ == '__main__':
	try:
		t = threading.Thread(target=hilo_var)
		t.start()
		app.run(port=3000)
	except KeyboardInterrupt:
		sys.exit()
