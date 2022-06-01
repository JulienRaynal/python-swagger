import json

from flask import request
from flask_restx import Namespace, Resource, fields

from database.database import request_database, execute_database

namespace: Namespace = Namespace("city", "city related endpoints")

city_model = namespace.model("City", {
    "id": fields.Integer(
        readonly=True,
        description="city id",
        required=False
    ),
    "name": fields.String(
        description="city name",
        required=True
    )
})

gare_from_city_model = namespace.model("Gare by city", {
    "city_name": fields.String(
        readonly=True,
        description="city name",
        required=False
    ),
    "station_name": fields.String(
        readonly=True,
        description="station name",
        required=False
    ),
    "station_id": fields.Integer(
        readonly=True,
        description="station id",
        required=False
    )
})


def convert_db_json(city: tuple) -> dict:
    return {
        "id": city[0],
        "name": city[1]
    }


def convert_station_city_json(station: tuple) -> dict:
    return {
        "city_name": station[0],
        "station_name": station[1],
        "station_id": station[2]
    }


@namespace.route('')
class CityGeneral(Resource):
    @namespace.marshal_list_with(city_model)
    @namespace.response(500, "Internal server error")
    def get(self) -> list:
        """Returns all the cities"""
        cities: list = request_database("SELECT * from Ville")
        json_cities: list = []
        for city in cities:
            json_cities.append(convert_db_json(city))
        return json_cities

    @namespace.expect(city_model)
    def post(self):
        """Create city"""
        json_data: json = request.json
        execute_database("INSERT INTO Ville (Nom)"
                         "VALUES ('{}')".format(json_data["name"]))


@namespace.route("/<int:id>")
@namespace.param("id", "the city id")
class City(Resource):
    @namespace.marshal_with(city_model)
    @namespace.response(500, "BDD error")
    def get(self, id) -> dict:
        """Get city with specific id"""
        city: list = request_database("SELECT * from Ville where Id={}".format(id))
        return {
            "id": city[0][0],
            "name": city[0][1]
        }

    def delete(self, id):
        """Delete user with specific id"""
        execute_database("DELETE FROM Ville where Id={}".format(id))


@namespace.route("/gare/<int:id>")
@namespace.param("id", "the city id")
class CityStations(Resource):
    @namespace.marshal_with(gare_from_city_model)
    @namespace.response(500, "BDD error")
    def get(self, id) -> list:
        """Get station with specific city id"""
        stations: list = request_database(
            "SELECT V.Nom, Gare.Nom, Gare.Id FROM Gare JOIN Dessert D on Gare.Id = D.IdGare JOIN Ville V on D.IdVille = V.Id WHERE D.IdVille = {};".format(
                id))
        json_stations: list = []
        for station in stations:
            json_stations.append(convert_station_city_json(station))
        return json_stations
