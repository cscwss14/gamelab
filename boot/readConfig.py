import json
from pprint import pprint

def config():
	with open('data.json') as data_file:    
    		data = json.load(data_file)

	return data
