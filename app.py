import re
from flask import Flask, jsonify, request
from pymongo import MongoClient
 


app = Flask(__name__)
db = MongoClient('localhost').get_database('octopus')

@app.route('/', methods=['GET'])
def get_home():
    return jsonify({
        'app_name': 'railways-api',
        'version': '0.1'
    })

@app.route('/stations', methods=['GET'])
def get_stations():
    stations = list(db.stations.find())
    return jsonify(stations)

@app.route('/stations', methods=['POST'])
def add_station():
    json_data = request.get_json()
    station_id = "".join(re.findall(r'[a-zA-Z]', json_data["name"])).lower()
    station_name = json_data["name"]
    station_city = json_data["city"]       
    db.stations.insert({"_id":station_id, "name":station_name, "city":station_city})
    
    return jsonify({"id":station_id})     
 