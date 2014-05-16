import json
from pprint import pprint

def config():
	with open('data.json') as data_file:    
    		data = json.load(data_file)

	return data

def orientation():
	with open('OrientationData.json') as data_file:
        	orient = json.load(data_file)

        return orient

def connectionInfo():
	with open('ConnectionPointData.json') as data_file:
		connInfo = json.load(data_file)
        
	return connInfo

def read_pixel_info():
	with open('Pixel_Info.json') as data_file:
		pixel_info = json.load(data_file)
        
	return pixel_info
