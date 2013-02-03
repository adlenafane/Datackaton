import requests
from requests.auth import HTTPDigestAuth
import pprint

AUTH = HTTPDigestAuth("Datackathon","31c622990a5aa4912341af729f8e418abd0bb56d")

def getAllRestaurants():
	url = "http://api.mobimenu.fr/restaurants/1.json?max_page"
	res = requests.get(url, auth=AUTH)
	max_page = res.json()['max_page']
	
	# Get restaurants list
	dicOfAllRestaurants = {}
	for i in range(1, max_page):
		url = "http://api.mobimenu.fr/restaurants/"+str(i)+".json"
		res = requests.get(url, auth=AUTH)
		res_json = res.json()
		for j in range(0, 100):
			rest_name = res_json['restaurant'][j]['name']
			rest_id = res_json['restaurant'][j]['id']
			rest_city = res_json['restaurant'][j]['city']
			listOfAllRestaurants.append([rest_name, rest_id, rest_city])
	return listOfAllRestaurants