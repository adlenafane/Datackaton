# -*- coding: utf-8 -*-

"""
    Wine suggestion
    ~~~~~~
    Datackathon - Application pour suggérer le meilleure vin pour un plate donné
    Utilisation d'API de 1001 menus
"""

from flask import Flask, render_template, request
import requests, pprint
from requests.auth import HTTPDigestAuth

app = Flask(__name__)
AUTH = HTTPDigestAuth("Datackathon","31c622990a5aa4912341af729f8e418abd0bb56d")

@app.route('/')
def home_page():                                                                    
	return render_template('layout.html')

@app.route('/getResults')
def getResults():
	restaurant = request.args.get('restaurant', '')

	'''Get restaurant ID A FAAAAAAAIRE'''
	rest_id = int(restaurant)
	url = "http://api.mobimenu.fr/restaurant/"+str(rest_id)+".json"
	res = requests.get(url, auth=AUTH)
	res_json = res.json()
	listMenuID = res.json()['restaurant']['menu']['menu_id']
	allLabels = []
	for menu_id in listMenuID:
		url = "http://api.mobimenu.fr/menu/"+str(menu_id)+".json"
		resMenu = requests.get(url, auth=AUTH)
		categories = resMenu.json()['menu']
		for category in categories:
			subcategories = categories['category']
			for subcategory in subcategories:
				pprint.pprint(subcategory)
				try:
					subsubcategories=subcategory['subcategory']
					for subsubcategory in subsubcategories:
						try:
							dishes = subsubcategory['dishes']
							for dish in dishes:
								dish = dishes['dish']
								for indices in range(len(dish)):
									labels = dish[indices]['label']
									allLabels.append(labels)
						except:
							for indices2 in range(0, len(dishes)):
								dishes = subsubcategory[indices2]['dishes']
								for dish in dishes:
									dish = dishes['dish']
									for indices in range(len(dish)):
										labels = dish[indices]['label']
										allLabels.append(labels)	
				except:
					try:
						dishes = subcategory['dishes']
						for dish in dishes:
							dish = dishes['dish']
							for indices in range(len(dish)):
								labels = dish[indices]['label']
								allLabels.append(labels)
					except:
						for indices2 in range(0, len(dishes)):
							dishes = subcategory[indices2]['dishes']
						for dish in dishes:
							dish = dishes['dish']
							for indices in range(len(dish)):
								labels = dish[indices]['label']
								allLabels.append(labels)


	return render_template('layout_plat.html', plats = allLabels, test='')

@app.route('/getWine/<plat>')
def getBestWine(plat):
	vins = ['Chateau X', 'Chateau Y']
	return render_template("layout_wine.html", plat=plat, wines = vins)

if __name__ == '__main__':
    #init_db()
    app.run(debug=True)