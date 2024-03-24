#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from app import app
from app import database
from flask import render_template, request, url_for
import os
import sys
import time

@app.route('/', methods=['POST','GET'])
@app.route('/index', methods=['POST','GET'])
def index():
    return render_template('index.html')


@app.route('/borraEstado', methods=['POST','GET'])
def borraEstado():
    if 'state' in request.form:
        state    = request.form["state"]
        bSQL    = request.form["txnSQL"]
        bCommit = "bCommit" in request.form
        bFallo  = "bFallo"  in request.form
        duerme  = request.form["duerme"]
        dbr = database.delState(state, bFallo, bSQL=='1', int(duerme), bCommit)
        return render_template('borraEstado.html', dbr=dbr)
    else:
        return render_template('borraEstado.html')

    
@app.route('/topUK', methods=['POST','GET'])
def topUK():
    # TODO: consultas a MongoDB ...
    movies=[[],[],[]]
    return render_template('topUK.html', movies=movies)

@app.route('/borraCiudad', methods=['GET', 'POST'])
def borraCiudad():
    if request.method == 'POST':
        ciudad = request.form['ciudad']
        resultado = borrar_clientes_ciudad(ciudad)
        return render_template('resultado_borrado.html', resultado=resultado)
    return render_template('formulario_borra_ciudad.html')