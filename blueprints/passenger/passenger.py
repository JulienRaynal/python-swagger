import json

from flask import request
from flask_restx import Namespace, Resource, fields

from database.database import request_database, execute_database

namespace: Namespace = Namespace("passenger", "passenger related endpoints")

passenger_model = namespace.model("Passenger", {
    "id": fields.Integer(
        readonly=True,
        description="Passenger id",
        required=False
    ),
    "name": fields.String(
        description="Passenger name",
        required=True
    ),
    "surname": fields.String(
        description="Passenger surname",
        required=True
    )
})


def convert_db_json(passenger: tuple) -> dict:
    return {
        "id": passenger[0],
        "name": passenger[1],
        "surname": passenger[2],
    }


@namespace.route('')
class PassengerGeneral(Resource):
    @namespace.marshal_list_with(passenger_model)
    @namespace.response(500, "Internal server error")
    def get(self) -> list:
        """Returns all the passengers"""
        passengers: list = request_database("SELECT * FROM Passager")
        json_passengers: list = []
        for passenger in passengers:
            json_passengers.append(convert_db_json(passenger))
        return json_passengers

    @namespace.expect(passenger_model)
    def put(self):
        """Create a passenger"""
        json_data: json = request.json
        execute_database("INSERT INTO Passager (Nom, Prenom)"
                         "VALUES ('{}', '{}')".format(
            json_data["name"],
            json_data["surname"]
        ))


@namespace.route("/<int:id>")
@namespace.param("id", "the passenger id")
class Passenger(Resource):
    @namespace.marshal_list_with(passenger_model)
    @namespace.response(500, "BDD error")
    def get(self, id) -> dict:
        """Get passenger with specific id"""
        passenger: list = request_database("SELECT * from Passager where Id={}".format(id))
        return passenger[0]

    def delete(self, id):
        """Delete user with specific id"""
        execute_database("DELETE FROM Passager where Id={}".format(id))

    @namespace.expect(passenger_model)
    def post(self, id):
        """modify a passenger"""
        datas_dict: dict = {}
        for key in request.json:
            if key == "name" and request.json.get(key) != "string" and request.json.get(key) is not None:
                execute_database("UPDATE Passager SET Nom = '{}' WHERE Id={}".format(request.json.get(key), id))
            if key == "surname" and request.json.get(key) != "string" and request.json.get(key) is not None:
                execute_database("UPDATE Passager SET Prenom = '{}' WHERE Id={}".format(request.json.get(key), id))
