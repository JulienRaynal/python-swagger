import json

from flask import request
from flask_restx import Namespace, Resource, fields

from database.database import request_database, execute_database

namespace: Namespace = Namespace("station", "station related endpoints")

station_model = namespace.model("Station", {
    "id": fields.Integer(
        readonly=True,
        description="Station id",
        required=False
    ),
    "name": fields.String(
        description="Station name",
        required=True
    ),
    "idCity": fields.Integer(
        description="City id the station is in",
        required=True
    )
})

station_train_model = namespace.model("Trains that reach the station", {
    "train_id": fields.Integer(
        readonly=True,
        description="Train id",
    ),
    "train_departure_date": fields.String(
        readonly=True,
        description="The date the train is leaving"
    ),
    "train_company_name": fields.String(
        readonly=True,
        description="name of the train company"
    ),
    "train_company_id": fields.Integer(
        readonly=True,
        description="id of the train company"
    ),
    "arrival_time": fields.String(
        readonly=True,
        description="arrival time of the train at the station"
    ),
    "leaving_time": fields.String(
        readonly=True,
        description="leaving time of the train at the station"
    )
})


def convert_db_json(station: tuple) -> dict:
    return {
        "id": station[0],
        "name": station[1],
        "idCity": station[2]
    }


def convert_station_train_json(train: tuple) -> dict:
    return {
        "train_id": train[0],
        "train_departure_date": train[1],
        "train_company_name": train[2],
        "train_company_id": train[3],
        "arrival_time": train[4],
        "leaving_time": train[5]
    }


@namespace.route("")
class StationGeneral(Resource):
    @namespace.marshal_list_with(station_model)
    @namespace.response(500, "Internal server error")
    def get(self) -> list:
        """Returns all the stations"""
        stations: list = request_database("SELECT * FROM Gare")
        json_stations: list = []
        for station in stations:
            json_stations.append(convert_db_json(station))
        return json_stations

    @namespace.expect(station_model)
    def post(self):
        """Create a station"""
        json_data: json = request.json
        execute_database("INSERT INTO Gare (Nom, IdVille)"
                         "VALUES ('{}', '{}')".format(
            json_data["name"],
            json_data["idCity"]
        ))


@namespace.route("/<int:id>")
@namespace.param("id", "the station id")
class Station(Resource):
    @namespace.marshal_with(station_model)
    @namespace.response(500, "BDD error")
    def get(self, id) -> dict:
        """Get station with specific id"""
        station: list = request_database("SELECT * from Gare where Id={}".format(id))
        return station[0]

    def delete(self, id):
        """Delete station with specific id"""
        execute_database("DELETE FROM Gare where Id={}".format(id))


@namespace.route("/trains/<int:id>")
@namespace.param("id", "the station id")
class StationTrains(Resource):
    @namespace.marshal_list_with(station_train_model)
    @namespace.response(500, "BDD error")
    def get(self, id) -> list:
        """Gets all the trains that go through this station"""
        trains: list = request_database("SELECT T.Numero, T.DateDep, C.Nom, C.Id, A.HeureArrive, A.HeureDep \
                                            FROM Gare JOIN Arret A on Gare.Id = A.IdGare \
                                            JOIN Train T on A.IdTrain = T.Numero JOIN Companie C on T.IdCompanie = C.Id \
                                            WHERE Gare.Id = {};".format(id))
        json_trains: list = []
        for train in trains:
            json_trains.append(convert_station_train_json(train))
        return json_trains
