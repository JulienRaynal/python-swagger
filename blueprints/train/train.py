import json

from flask import request
from flask_restx import Namespace, fields, Resource

from database.database import request_database, execute_database

namespace: Namespace = Namespace("train", "train related endpoints")

train_model = namespace.model("Train", {
    "Numero": fields.Integer(
        readonly=True,
        description="Client id",
        required=False
    ),
    "HeureDep": fields.String(
        description="Departure time",
        required=True
    ),
    "HeureArrive": fields.String(
        description="Arrival time",
        required=True
    ),
    "DateDep": fields.String(
        description="Departure date",
        required=True,
    ),
    "DateArrive": fields.String(
        description="Arrival time",
        required=True
    ),
    "IdCompanie": fields.Integer(
        description="Companie Id",
        required=True
    )
})


def convert_db_json(train: tuple) -> dict:
    return {
        "Numero": train[0],
        "HeureDep": train[1],
        "HeureArrive": train[2],
        "DateDep": train[3],
        "DateArrive": train[4],
        "IdCompanie": train[5]
    }


@namespace.route('')
class TrainGeneral(Resource):
    @namespace.marshal_list_with(train_model)
    @namespace.response(500, "Internal server error")
    def get(self) -> list:
        """Returns all the trains"""
        trains: list = request_database("SELECT * FROM Train")
        json_trains: list = []
        for train in trains:
            json_trains.append(convert_db_json(train))
        return json_trains

    @namespace.expect(train_model)
    @namespace.response(500, "Internal server error")
    def post(self):
        """Create train"""
        json_data: json = request.json
        execute_database("INSERT INTO Train (HeureDep, HeureArrive, DateDep, DateArrive, IdCompanie)"
                         "VALUES ('{}', '{}', '{}', '{}', '{}')".format(
            json_data["HeureDep"],
            json_data["HeureArrive"],
            json_data["DateDep"],
            json_data["DateArrive"],
            json_data["IdCompanie"]
        ))

    @namespace.route("/<int:id>")
    @namespace.param("id", "the train id")
    class Train(Resource):
        @namespace.marshal_list_with(train_model)
        @namespace.response(500, "BDD error")
        def get(self, id) -> dict:
            """Get train with specific id"""
            client: list = request_database("SELECT * from Train where Id={}".format(id))
            return client[0]

        def delete(self, id):
            """Delete train with specific id"""
            execute_database("DELETE FROM Train where Id={}".format(id))
