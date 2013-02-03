import requests, pprint, json
import cPickle as pickle
from requests.auth import HTTPDigestAuth
from progressbar import *

AUTH = HTTPDigestAuth("Datackathon","31c622990a5aa4912341af729f8e418abd0bb56d")

def getAllRestaurants():
	url = "http://api.mobimenu.fr/restaurants/1.json?max_page"
	res = requests.get(url, auth=AUTH)
	max_page = res.json()['max_page']
	
	widgets = ['Test: ', Percentage(), ' ', Bar(marker='>',left='[',right=']'), ' ', ETA(), ' ', FileTransferSpeed()] #see docs for other options

	pbar = ProgressBar(widgets=widgets, maxval=500)
	pbar.start()
	# Get restaurants list
	dicOfAllRestaurants = {}
	for i in range(1, max_page):
		url = "http://api.mobimenu.fr/restaurants/"+str(i)+".json"
		res = requests.get(url, auth=AUTH)
		res_json = res.json()
		listOfJson = []
		for j in range(0, 99):
			try:
				rest_name = res_json['restaurant'][j]['name']
				rest_id = res_json['restaurant'][j]['id']
				rest_city = res_json['restaurant'][j]['city']
				jsonElement = "{'name': "+str(rest_name)+", 'id': "+str(rest_id)+", 'city': "+str(rest_city)+"}"
				dicOfAllRestaurants[rest_name] = [rest_id, rest_city]
				listOfJson.append(jsonElement)
			except:
				pass
		pbar.update(i)
	pbar.finish()
	print "length", len(dicOfAllRestaurants)
	with open('data/restaurants.json', 'wb') as f:
		json.dump(dicOfAllRestaurants, f)
	with open('data/restaurants2.txt', 'wb') as f:
		pickle.dump(listOfJson, f)

#getAllRestaurants()