#!/usr/bin/env python
# -*- coding: utf-8 -*-

import threading
import time
from random import randint
import numpy as np
import sys

from flask import Flask, url_for, jsonify
from flask.ext.cors import CORS, cross_origin
app = Flask(__name__)

temp = 0
contador = 0

def hilo_temp():
    global temp, contador
    while True:
        # modifica la temperatura cada 5 segundo
        if contador % 5 == 0:
            mu, sigma = 98.2249, 0.733 # media y desvstd
            temp = np.random.normal(mu, sigma)
            temp = (temp - 32) * 5.0/9.0 # fahren a celsius
            temp = round(temp, 2)
        contador += 1
        time.sleep(1)


@app.route('/')
@cross_origin() 
def api_root():
    global temp
    res = {'temperatura': temp}
    return jsonify(**res)

if __name__ == '__main__':
    try:
        t = threading.Thread(target=hilo_temp)
        t.start()
        app.run(port=3000)
    except KeyboardInterrupt:
        sys.exit()
