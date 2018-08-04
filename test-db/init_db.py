import datetime
from pymongo import MongoClient


stations = [
    { "_id": "parisest", "name": "Paris-Est", "city": "Paris"},
    { "_id": "parisnord", "name": "Paris-Nord", "city": "Paris"},
    { "_id": "parissaintlazare", "name": "Paris-Saint-Lazare", "city": "Paris"},
    { "_id": "parisausterlitz", "name": "Paris-Austerlitz", "city": "Paris"},
    { "_id": "parismontparnasse", "name": "Paris-Montparnasse", "city": "Paris"},
    { "_id": "bordeauxsaintjean", "name": "Bordeaux-Saint-Jean", "city": "Bordeaux"},
    { "_id": "reims", "name": "Reims", "city": "Reims"},
    { "_id": "chalonsenchampagne", "name": "Châlons-en-Champagne", "city": "Chalons-en-Champagne"},
    { "_id": "trouvilledeauville", "name": "Trouville-Deauville", "city": "Deauville"},
    { "_id": "tourssaintpierredescorps", "name": "Tours-Saint-Pierre-des-Corps", "city": "Tours"},
    { "_id": "lilleflandres", "name": "Lille-Flandres", "city": "Lille"},
    { "_id": "orleanslesaubrais", "name": "Orléans-les-Aubrais", "city": "Orléans"},
]


lines = [
    { "_id": "parisausterlitz-bordeauxsaintjean", "name": "Paris - Bordeaux", "stops": ["parisausterlitz", "orleanslesaubrais", "tourssaintpierredescorps", "bordeauxsaintjean"] },
    { "_id": "parisest-chalonsenchampagne",  "name": "Paris - Chalons-en-Champagne", "stops": ["parisest", "reims", "chalonsenchampagne"] },
]

trips = [
    {
        "_id": "6f8af364-7408-48a2-b922-e861467c0e59",
        "line": "parisest-chalonsenchampagne",
        "stops" : [
            {
                "station_id": "parisest",
                "departure_time": datetime.datetime(2018, 8, 1, 18, 0),
                "platform": "22",
                "remaining_seats": 40
            },
            {
                "station_id": "reims",
                "arrival_time": datetime.datetime(2018, 8, 1, 19, 0),
                "departure_time": datetime.datetime(2018, 8, 1, 19, 5),
                "platform": "2",
                "remaining_seats": 140
            },
            {
                "station_id": "chalonsenchampagne",
                "arrival_time": datetime.datetime(2018, 8, 1, 20, 0),
                "platform": "1",
            }
        ]

    }
]


def main():
    client = MongoClient('localhost:27017')
    stations_coll = client['octopus']['stations']
    stations_coll.delete_many({})
    lines_coll = client['octopus']['lines']
    lines_coll.delete_many({})
    trips_coll = client['octopus']['trips']
    trips_coll.delete_many({})
    for station in stations:
        stations_coll.insert(station)
    for line in lines:
        lines_coll.insert(line)
    for trip in trips:
        trips_coll.insert(trip)

if __name__ == '__main__':
    main()