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

def hilo_temp():
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
        t = threading.Thread(target=hilo_temp)
        t.start()
        app.run(port=3000)
    except KeyboardInterrupt:
        sys.exit()
