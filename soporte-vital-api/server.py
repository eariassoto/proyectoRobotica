#!/usr/bin/env python

import threading
import time
from random import randint

temp = 0;

from flask import Flask, url_for
from flask.ext.cors import CORS, cross_origin
app = Flask(__name__)

def hilo_temp():
    global temp
    while True:
        temp = 30 + randint(0,9)
        time.sleep(5)


@app.route('/')
@cross_origin() 
def api_root():
    return 'Welcome'

@app.route('/temperatura')
@cross_origin()
def api_articles():
    global temp
    return 'Temperatura ' + str(temp) #'List of ' + url_for('api_articles')

@app.route('/articles/<articleid>')
def api_article(articleid):
    return 'You are reading ' + articleid

if __name__ == '__main__':
    t = threading.Thread(target=hilo_temp)
    t.start()
    app.run(port=3000)

