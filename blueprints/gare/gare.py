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


def convert_db_json(station: tuple) -> dict:
    return {
        "id": station[0],
        "name": station[1],
        "idCity": station[2]
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
