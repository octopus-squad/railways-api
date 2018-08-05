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


@app.route('/station/<id>', methods=['GET'])
def get_station(id):
    stations = list(db.stations.find())
    for station in stations:
        if id == station["_id"]:
            return_station = {
                "name" : station["name"],
                "city" : station["city"],
                "id" : station["_id"]
            }
    
    return jsonify(return_station)


@app.route('/stations', methods=['POST'])
def add_station():
    json_data = request.get_json()

    station_id = "".join(re.findall(r'[a-zA-Z]', json_data["name"])).lower()
    station_name = json_data["name"]
    station_city = json_data["city"]       
    db.stations.insert({"_id":station_id, "name":station_name, "city":station_city})
    
    return jsonify({"id":station_id})     


@app.route('/stations/<id>', methods=['DELETE'])
def delete_station(id):
    db.stations.remove({"_id": id})    
    return jsonify({"id":id})
            

@app.route('/station/<id>', methods=['PUT'])
def update_station(id):
    json_data = request.get_json()
    db.stations.update(
        {"_id":id},
        {"$set":
        {
            "name":json_data["name"],
            "city" :json_data["city"]
            }
            }
        )
    
    return jsonify({"id":id})
