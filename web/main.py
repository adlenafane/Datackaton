# -*- coding: utf-8 -*-

"""
    Wine suggestion
    ~~~~~~
    Datackathon - Application pour suggérer le meilleure vin pour un plate donné
    Utilisation d'API de 1001 menus
"""

from flask import Flask, render_template, request
import requests, pprint
import cPickle
from requests.auth import HTTPDigestAuth
from dataRetrieving import getAllRestaurants

app = Flask(__name__)
AUTH = HTTPDigestAuth("Datackathon","31c622990a5aa4912341af729f8e418abd0bb56d")
'''
with open('data/restaurants.json', 'rb') as f:
	restaurantJson = json.load(f)'''
with open('data/restaurants2.txt', 'rb') as f:
	restaurantsJsonFlat = f.readlines()

@app.route('/')
def home_page():
	url = "http://api.mobimenu.fr/restaurants/1.json"
	res = requests.get(url, auth=AUTH)
	res_json = res.json()
	
	return render_template('layout_restaurant.html', next_page = "2", restaurants = res_json['restaurant'], restaurantsJsonFlat = restaurantsJsonFlat)

@app.route('/<page>')
def restaurant_page(page):
	url = "http://api.mobimenu.fr/restaurants/"+str(page)+".json"
	res = requests.get(url, auth=AUTH)
	res_json = res.json()
	next = int(page)+1
	next = str(next)
	return render_template('layout_restaurant.html', next_page = next, restaurants = res_json['restaurant'])

@app.route('/getResults/<restaurant>')
def getResults(restaurant):
	rest_id = restaurant

	'''Get restaurant ID A FAAAAAAAIRE'''
	rest_id = int(rest_id)
	url = "http://api.mobimenu.fr/restaurant/"+str(rest_id)+".json"
	resMenu = requests.get(url, auth=AUTH)

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
						try:
							for indices2 in range(0, len(dishes)):
								dishes = subcategory[indices2]['dishes']
								for dish in dishes:
									dish = dishes['dish']
									for indices in range(len(dish)):
										labels = dish[indices]['label']
										allLabels.append(labels)
						except:
							pass

	return render_template('layout_plat.html', plats = allLabels, test='')

@app.route('/test')
def test():
	return render_template('layout.html')

@app.route('/getWine/<plat>')
def getBestWine(plat):
	vins = ['Chateau X', 'Chateau Y']
	return render_template("layout_wine.html", plat=plat, wines = vins)

if __name__ == '__main__':
    app.run(debug=True)