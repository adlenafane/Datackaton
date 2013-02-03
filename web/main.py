# -*- coding: utf-8 -*-

"""
    Wine suggestion
    ~~~~~~
    Datackathon - Application pour suggérer le meilleure vin pour un plate donné
    Utilisation d'API de 1001 menus
"""

from flask import Flask, render_template, request
import requests
from requests.auth import HTTPDigestAuth

app = Flask(__name__)
AUTH = HTTPDigestAuth("Datackathon","31c622990a5aa4912341af729f8e418abd0bb56d")

@app.route('/')
def home_page():                                                                    
	return render_template('layout.html')

@app.route('/getResults')
def getResults():
	plat = request.args.get('plat', '')
	vins = [['NomDeVin1', 'Description1'], ['NomDeVin2', 'Description2']]
	return render_template('layout_result.html', vins = vins, plat = plat)

if __name__ == '__main__':
    #init_db()
    app.run(debug=True)