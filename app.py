# -*- coding: utf-8 -*-

from flask import Flask, render_template, request, jsonify
from flask_mysqldb import MySQL

from datetime import datetime
import sys
import json
import unicodedata


app = Flask(__name__)


app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'MyDB'

mysql = MySQL(app)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        firstName = 'first'
        lastName = 'last'
        cur = mysql.connection.cursor()
        cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
        mysql.connection.commit()
        cur.close()
        return 'success'
    return 'hi'
	
@app.route('/add', methods=['GET'])
def add():
	firstName = 'first'
	lastName = 'last'
	cur = mysql.connection.cursor()
	cur.execute("INSERT INTO MyUsers(firstName, lastName) VALUES (%s, %s)", (firstName, lastName))
	mysql.connection.commit()
	cur.close()
	return 'success'
	
	
def err_resp(str, code):
	message = {
		'error': str
	}
	resp = jsonify(message)
	resp.status_code = code
	return resp	
	
@app.route('/imports', methods=['POST'])
def add_user():


	_json = request.json
	
	
	print('json: ', _json, type(_json), file=sys.stderr)

	relativesDic=dict()
	
	#parse
	for citizen in _json.get('citizens'):
		#print('hi, id: ', citizen['citizen_id'], file=sys.stderr)
		citizen_id = citizen.get('citizen_id')
		town = citizen.get('town')
		street = citizen.get('street')
		building = citizen.get('building')
		apartment = citizen.get('apartment')
		name = citizen.get('name')
		birth_date = citizen.get('birth_date')
		gender = citizen.get('gender')
		relatives = citizen.get('relatives')
		
		
		
		if not (citizen_id and town and street and building and apartment and name and birth_date and gender and relatives):
			return err_resp('empty fields', 400)
		
		if len(citizen) != 9:
			return err_resp('unneccasary fields', 400)
		
		try:
			value = int(citizen_id)
			value = int(apartment)
		except ValueError:
			return err_resp('bad int param', 400)
			
		if	citizen_id <=0 or apartment <=0:
			return err_resp('bad int param', 400)
		
		if	len(name) > 256 or len(town) > 256 or len(street) > 256 or len(building) > 256:
			return err_resp('bad str param', 400)

		
		#date
		try:
			citizen['birth_date'] = datetime.strptime(birth_date, "%d.%m.%Y").strftime("%Y-%m-%d")
		except ValueError:
			return err_resp('bad date param', 400)
			
		if citizen['birth_date'] > datetime.today().strftime('%Y-%m-%d'):
			return err_resp('bad date param, greater then current moment', 400)
			
		#gender			
		if not (gender == 'male' or gender == 'female'):
			return err_resp('bad gender param', 400)
		
		
		
		
		print('list of rel: ', list(citizen['relatives']), file=sys.stderr)
		relativesDic[citizen_id]=list(citizen['relatives'])
		print('relativesDic: ', relativesDic, file=sys.stderr)
		
		#adding to collection
		
	
	#relatives
	try:
		for person in relativesDic:
			for rel in relativesDic[person]:
				if not person in relativesDic[rel]:
					message = {
						'error': 'bad relatives'
					}
					resp = jsonify(message)
					resp.status_code = 400
					return resp
	
	except Exception as e:
		message = {
			'error': 'bad relatives exc'
		}
		resp = jsonify(message)
		resp.status_code = 400
		return resp
	
	#print('relDIc: ', relativesDic, file=sys.stderr)
	
	
	
	#adding to db
	
	#adding import_id
	conn = mysql.connect
	cur = conn.cursor()
	cur.execute("INSERT INTO imports VALUES()")
	#conn.commit()
	cur.execute("SELECT LAST_INSERT_ID()")
	for row in cur:
		 import_id=row[0]			 
	
	
	#adding person
	for citizen in _json.get('citizens'):
		#print('hi, id: ', citizen['citizen_id'], file=sys.stderr)
		citizen_id = citizen.get('citizen_id')
		town = citizen.get('town')
		street = citizen.get('street')
		building = citizen.get('building')
		apartment = citizen.get('apartment')
		name = citizen.get('name')
		birth_date = citizen.get('birth_date')
		gender = citizen.get('gender')
		relatives = citizen.get('relatives')
		

		sql = "INSERT INTO persons(import_id, citizen_id, town, street, building, apartment, name, birth_date, gender) VALUES(%s, %s, %s, %s, %s, %s, %s, %s, %s)"
		data = (import_id, citizen_id, town, street, building, apartment, name, birth_date, gender,)
		cur.execute(sql, data)
		#conn.commit()
	
	#adding rels
	for person in relativesDic:
			for rel in relativesDic[person]:
				sql = "INSERT INTO relatives ( relative, import_id, citizen_id) VALUES(%s, %s, %s)"
				data = ( rel, import_id, person)
				cur.execute(sql, data)
				#conn.commit()
	
	conn.commit()
	cur.close() 
	conn.close()
	
	inmsg = {'import_id': import_id}
	message = {
	'data': inmsg
	}
	
	resp = jsonify(message)
	resp.status_code = 200
	return resp
		
'''
except Exception as e:
	return str(e)
	#return jsonify({'error': 'error'})
finally:
'''


	#mysql.connection.close()
		
	
@app.route('/imports/<int:import_id>/citizens/<int:citizen_id>', methods=['PATCH'])
def change_user(import_id, citizen_id):	

	_json = request.json
	print('_json',type(_json), _json, file=sys.stderr)

	
	#parse
	town = _json.get('town')
	street = _json.get('street')
	building = _json.get('building')
	apartment = _json.get('apartment')
	name = _json.get('name')
	birth_date = _json.get('birth_date')
	gender = _json.get('gender')
	relatives = _json.get('relatives')
	
	if not (town or street or building or apartment or name or birth_date or gender or relatives):
		message = {
			'error': 'empty fields'
		}
		resp = jsonify(message)
		resp.status_code = 400
		return resp
	
	#checking existence
	
	#updating
	conn = mysql.connect
	cur = conn.cursor()
	
	cur.execute("SELECT 1 FROM persons WHERE import_id=%s and citizen_id=%s", (import_id, citizen_id))
	print('len num for person exists', len(list(cur)), file=sys.stderr)
	if len(list(cur)) < 1:
		message = {
		'error': 'person doesnt exist'
		}
		resp = jsonify(message)
		resp.status_code = 400
		return resp
	
	#i know, that's very bad, but it is about my time limits ((
	print('town ',town, file=sys.stderr)
	if town:
		cur.execute("UPDATE persons SET town = %s WHERE import_id=%s and citizen_id=%s", (town, import_id, citizen_id))
	if street:
		cur.execute("UPDATE persons SET street = %s WHERE import_id=%s and citizen_id=%s", (street, import_id, citizen_id))
	if building:
		cur.execute("UPDATE persons SET building = %s WHERE import_id=%s and citizen_id=%s", (building, import_id, citizen_id))
	if apartment:
		cur.execute("UPDATE persons SET apartment = %s WHERE import_id=%s and citizen_id=%s", (apartment, import_id, citizen_id))
	if name:
		cur.execute("UPDATE persons SET name = %s WHERE import_id=%s and citizen_id=%s", (name, import_id, citizen_id))
	if birth_date:
		try:
			birth_date = datetime.strptime(birth_date, "%d.%m.%Y").strftime("%Y-%m-%d")
		except ValueError:
			message = {
				'error': 'bad date'
			}
			resp = jsonify(message)
			resp.status_code = 400
			return resp
		cur.execute("UPDATE persons SET birth_date = %s WHERE import_id=%s and citizen_id=%s", (birth_date, import_id, citizen_id))
	if gender:
		if not (gender == 'male' or gender == 'female'):
			message = {
				'error': 'bad gender'
			}
			resp = jsonify(message)
			resp.status_code = 400
			return resp
		
		cur.execute("UPDATE persons SET gender = %s WHERE import_id=%s and citizen_id=%s", (gender, import_id, citizen_id))
	
	
	#rels
	rels=_json.get('relatives')
	print('rels:  ',rels,type(rels), file=sys.stderr)

	if rels:
		for rel in rels:
			print('rel num',rel, file=sys.stderr)
			cur.execute("SELECT 1 FROM persons WHERE import_id=%s and citizen_id=%s", (import_id, rel))
			
			print('len num', len(list(cur)), file=sys.stderr)
			if len(list(cur)) < 1:
				message = {
				'error': 'person in relatives dont exist'
				}
				resp = jsonify(message)
				resp.status_code = 400
				return resp
		
	cur.execute("SELECT relative FROM relatives WHERE import_id=%s and citizen_id=%s", (import_id, citizen_id))
	prevSet = set()
	for row in list(cur):
		prevSet.add(row[0])
	newSet = set(rels)
	diffToDelete=prevSet-newSet
	diffToAdd=newSet-prevSet
	
	
	
	print('diffToDelete ',diffToDelete, type(diffToDelete) ,file=sys.stderr)
	print('diffToAdd ',diffToAdd, type(diffToAdd) ,file=sys.stderr)
	
	print('prev ',prevSet,type(prevSet), file=sys.stderr)
	print('new ',newSet, type(newSet) ,file=sys.stderr)
	
	for rel in diffToAdd:
		cur.execute("INSERT INTO relatives ( relative, import_id, citizen_id) VALUES(%s, %s, %s)", (rel, import_id, citizen_id))
		if rel != citizen_id:
			cur.execute("INSERT INTO relatives ( relative, import_id, citizen_id) VALUES(%s, %s, %s)", (citizen_id, import_id, rel))

	for rel in diffToDelete:
		cur.execute("DELETE FROM relatives where relative=%s and import_id=%s and citizen_id=%s", (rel, import_id, citizen_id))
		cur.execute("DELETE FROM relatives where relative=%s and import_id=%s and citizen_id=%s", (citizen_id, import_id, rel))
	
				
			#sql = "INSERT INTO relatives ( relative, import_id, citizen_id) VALUES(%s, %s, %s)"
			#data = ( rel, import_id, citizen_id)
			#cur.execute(sql, data)
			
	
	
	conn.commit()
	
	print('imp cit ',import_id, citizen_id, file=sys.stderr)
	
	cur.execute("SELECT relative FROM relatives WHERE import_id=%s and citizen_id=%s", (import_id, citizen_id))
	relList = list()
	for row in list(cur):
		relList.append(row[0])
	
	cur.execute("SELECT citizen_id, town, street, building, apartment, name, DATE_FORMAT(birth_date, '%%d.%%m.%%Y') , gender FROM persons WHERE import_id=%s and citizen_id=%s", (import_id, citizen_id))
	rows = cur.fetchall()
	
	
	for row in cur:
		inmsg = {'citizen_id' : row[0], 
		'town' : row[1], 
		'street' : row[2], 
		'building' : row[3], 
		'apartment' : row[4], 
		'name' : row[5], 
		'birth_date' : row[6], 	
		'gender' : row[7],
		'relatives' : relList
		}
			
	message = {
      'data': inmsg
	}		
	resp = jsonify(message)
	resp.status_code = 200
	return resp
	
	cur.close() 
	conn.close()

@app.route('/imports/<int:import_id>/citizens', methods=['GET'])
def get_users(import_id):
	
	
	
	conn = mysql.connect
	cur = conn.cursor()
	
	#print('before ex ', file=sys.stderr)
	cur.execute("SELECT citizen_id FROM persons WHERE import_id=%s", (import_id,))
	#print('after ex ', file=sys.stderr)
	rows = list(cur)
	#print('rows ',rows, file=sys.stderr)

	
	citizensList=list()
	for row in rows:
		citizensList.append(row[0])
		
	inMessages = list()	
		
	for citizen_id in citizensList:
		
		cur.execute("SELECT relative FROM relatives WHERE import_id=%s and citizen_id=%s", (import_id, citizen_id))
		relList = list()
		for row in list(cur):
			relList.append(row[0])
		
		cur.execute("SELECT citizen_id, town, street, building, apartment, name, DATE_FORMAT(birth_date, '%%d.%%m.%%Y') , gender FROM persons WHERE import_id=%s and citizen_id=%s", (import_id, citizen_id))
		rows = cur.fetchall()
	
		
		inmsg = dict()	
		for row in cur:
			inmsg = {'citizen_id' : citizen_id, 
			'town' : row[1], 
			'street' : row[2], 
			'building' : row[3], 
			'apartment' : row[4], 
			'name' : row[5], 
			'birth_date' : row[6], 	
			'gender' : row[7],
			'relatives' : relList
			}
		
		inMessages.append(inmsg)
			
	message = {
      'data': inMessages
	}
	
	resp = jsonify(message)
	resp.status_code = 200
	return resp
	
	cur.close() 
	conn.close()
	

@app.route('/imports/<int:import_id>/citizens/birthdays', methods=['GET'])
def get_birthdays(import_id):
	
	conn = mysql.connect
	cur = conn.cursor()
	
	calenDict = dict()
	
	for i in range(1, 13):
		cur.execute("select  r.relative , count(p.citizen_id) FROM persons p INNER JOIN relatives r ON p.citizen_id = r.citizen_id AND p.import_id = r.import_id WHERE p.import_id = %s AND CAST(DATE_FORMAT(p.birth_date, '%%m') AS SIGNED) = %s Group by r.relative;", (import_id,i))
		rows = cur.fetchall()
		
		monthList = list()
		for row in rows:
			presDict = dict()
			print('i, row ', i, row, type(row), file=sys.stderr)
			presDict['citizen_id']=row[0]
			presDict['presents']=row[1]
			monthList.append(presDict)
			
		calenDict[i]=monthList
		
	print('calenDict ', calenDict, file=sys.stderr)

		
	
	message = {
      'data': calenDict
	}
	
	resp = jsonify(message)
	resp.status_code = 200
	return resp
	
	cur.close() 
	conn.close()
	
	
@app.route('/get')
def users():
	try:
		conn = mysql.connect()
		cursor = conn.cursor(pymysql.cursors.DictCursor)
		cursor.execute("SELECT * FROM persons")
		rows = cursor.fetchall()
		resp = jsonify(rows)
		resp.status_code = 200
		return resp
	except Exception as e:
		print(e)
	finally:
		cursor.close() 
		conn.close()
			
	
	

if __name__ == '__main__':
    #app.run(debug=True)
	app.config['JSON_AS_ASCII'] = False
	app.run(host='0.0.0.0', port=8080)
	
	
	
	
