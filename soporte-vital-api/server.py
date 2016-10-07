#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
from random import randint
import numpy as np

temp = 0;

from flask import Flask, url_for
from flask.ext.cors import CORS, cross_origin
app = Flask(__name__)

def hilo_temp():
    global temp
    while True:
        mu, sigma = 98.2249, 0.733 # media y desvstd
        temp = np.random.normal(mu, sigma)
        temp = (temp - 32) * 5.0/9.0 # fahren a celsius
        time.sleep(5)


@app.route('/')
@cross_origin() 
def api_root():
    return 'API Máquina Soporte Vital. v0.1'

@app.route('/temperatura')
@cross_origin()
def api_articles():
    global temp
    return 'Temperatura ' + str(temp)

if __name__ == '__main__':
    t = threading.Thread(target=hilo_temp)
    t.start()
    app.run(port=3000)
