import json

from flask import request
from flask_restx import Namespace, Resource, fields

from database.database import request_database, execute_database

namespace: Namespace = Namespace("stop", "train stops related endpoints")

stop_model = namespace.model("stop", {
    "arrivalTime": fields.String(
        description="arrival time at the stop",
        required=True
    ),
    "departureTime": fields.String(
        description="departure time at the stop",
        required=True
    ),
    "idStation": fields.Integer(
        description="stop id",
        required=True
    ),
    "idTrain": fields.Integer(
        description="related train id",
        required=True
    )
})


def convert_db_json(stop: tuple) -> dict:
    """converts tuple to json"""
    return {
        "arrivalTime": stop[0],
        "departureTime": stop[1],
        "idStation": stop[2],
        "idTrain": stop[3]
    }


@namespace.route('')
class stopGeneral(Resource):
    @namespace.marshal_list_with(stop_model)
    @namespace.response(500, "Internal server error")
    def get(self) -> list:
        stops: list = request_database("SELECT * FROM Arret")
        json_stop: list = []
        for stop in stops:
            json_stop.append(convert_db_json(stop))
        return json_stop

    @namespace.expect(stop_model)
    def post(self):
        """Create stop"""
        json_data: json = request.json
        execute_database("INSERT INTO Arret (HeureArrive, HeureDep, IdGare, IdTrain)"
                         "VALUES ('{}', '{}', '{}', '{}')".format(
            json_data["arrivalTime"],
            json_data["departureTime"],
            json_data["idStation"],
            json_data["idTrain"]
        ))


@namespace.route("/<int:id>")
@namespace.param("id", "the train id")
class stop(Resource):

    def delete(self, id):
        """Delete stop with specific train id"""
        execute_database("DELETE FROM Arret where IdTrain={}".format(id))
