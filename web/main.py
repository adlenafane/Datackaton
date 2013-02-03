# -*- coding: utf-8 -*-

"""
    Wine suggestion
    ~~~~~~
    Datackathon - Application pour suggérer le meilleure vin pour un plate donné
    Utilisation d'API ded 1001 menus
"""

from flask import Flask, render_template, request
import config1001

app = Flask(__name__)

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