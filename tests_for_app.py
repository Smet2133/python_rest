import requests
import json

def add_users():
	url = "http://127.0.0.1:5000/imports"

	payload = '{"citizens":[{"citizen_id":2,"town":"Москва","street":"Льва Толстого","building":"16к7стр5","apartment":7,"name":"Иванов Сергей Иванович","birth_date":"01.04.1997","gender":"male","relatives":[3,4]},{"citizen_id":3,"town":"Керчь","street":"Иосифа Бродского","building":"2","apartment":11,"name":"Романова Мария Леонидовна","birth_date":"23.11.1986","gender":"female","relatives":[2,3,4]},{"citizen_id":4,"town":"Керчь","street":"Иосифа Бродского","building":"2","apartment":11,"name":"Романова Мария Леонидовна","birth_date":"23.11.1986","gender":"female","relatives":[2,3]}]}'
	headers = {
    'Content-Type': "application/json",
    }

	response = requests.request("POST", url, data=payload, headers=headers)

	
	
	print(response.text.decode('unicode_escape'))
	
	
def get_users(import_id):
	import requests

	url = "http://127.0.0.1:5000/imports/{:d}/citizens".format(import_id)

	payload = ""
	headers = {
    'Content-Type': "application/json; charset=utf-8",
	
    }

	response = requests.request("GET", url, data=payload, headers=headers)
	response.encoding = 'utf-8'
	
	
	print(response.content.decode('utf-8'))
	
get_users(80)
