import re
from flask import Flask, jsonify, request
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


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


@app.route('/stations/<id>', methods=['GET'])
def get_station(id):
    station = list(db.stations.find_one({"_id":id}))
    if station is not None:
        return jsonify(station)
    else:
        error_response = jsonify({"error": "{} doesn't exist in database".format(id)})
        error_response.status_code = 400
        return error_response 


@app.route('/stations', methods=['POST'])
def add_station():
    json_data = request.get_json()
    try:
        station_id = "".join(re.findall(r'[a-zA-Z]', json_data["name"])).lower()
        station_name = json_data["name"]
        station_city = json_data["city"]
        db.stations.insert(
            {"_id": station_id, "name": station_name, "city": station_city})
        return jsonify({"id": station_id})
    except KeyError as e:
        error_response = jsonify({"error": "missing data: {}".format(e)})
        error_response.status_code = 400
        return error_response
    except DuplicateKeyError:
        error_response = jsonify({"error": "station already in database"})
        error_response.status_code = 400
        return error_response


@app.route('/stations/<id>', methods=['DELETE'])
def delete_station(id):
    db.stations.remove({"_id": id})
    return jsonify({"id": id})


@app.route('/stations/<id>', methods=['PUT'])
def update_station(id):
    json_data = request.get_json()
    db.stations.update(
        {"_id": id},
        {"$set":
         {
             "name": json_data["name"],
             "city": json_data["city"]
         }
         }
    )
    return jsonify({"id": id})


@app.route('/lines', methods=['GET'])
def get_lines():
    lines = list(db.lines.find())
    return jsonify(lines)


@app.route('/lines/<id>', methods=['GET'])
def get_line(id):
        line = db.lines.find_one({"_id":id})
        if line is not None:
            return jsonify(line)
        else:
            error_response = jsonify({"error": "{} doesn't exist in database".format(id)})
            error_response.status_code = 400
            return error_response


@app.route('/lines', methods=['POST'])
def add_line():
    try:
        json_data = request.get_json()
        line_id = "".join(re.findall(r'[a-zA-Z]', json_data["name"])).lower()
        line_name = json_data["name"]
        line_stops = json_data["stops"]
        db.lines.insert({"_id":line_id, "name":line_name, "stops":line_stops})
        return jsonify({"id": line_id})
    except KeyError as e:
        error_response = jsonify({"error": "missing data: {}".format(e)})
        error_response.status_code = 400
        return error_response
    except DuplicateKeyError:
        error_response = jsonify({"error": "line already in database"})
        error_response.status_code = 400
        return error_response
    

@app.route('/lines/<id>', methods=['DELETE'])
def delete_line(id):
    db.lines.remove({"_id": id})
    return jsonify({"id": id})


@app.route('/lines/<id>', methods=['PUT'])
def update_line(id):
    json_data = request.get_json()
    db.lines.update(
        {"_id": id},
        {"$set":
         {
             "name": json_data["name"],
             "stops": json_data["stops"]
         }
         }
    )
    return jsonify({"id": id})


@app.route('/trips', methods=['GET'])
def get_trips():
    trips = list(db.trips.find())
    return jsonify(trips)


# @app.route('/trips/<id>', methods=['GET'])
# def get_trips(id):
#         trip = db.trips.find_one({"_id":id})
#         if trip is not None:
#             return jsonify(trip)
#         else:
#             error_response = jsonify({"error": "{} doesn't exist in database".format(id)})
#             error_response.status_code = 400
#             return error_response


@app.route('/search/stations', methods=['GET'])
def search_stations():
    arg = request.args['arg']
    regex=re.compile(".*({}).*".format(arg))
    station = list(db.stations.find({ "city": regex })) 
    return jsonify(station)