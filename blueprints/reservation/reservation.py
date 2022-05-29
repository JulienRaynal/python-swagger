import json
from flask import request
from flask_restx import Namespace, Resource, fields

from database.database import request_database, execute_database

namespace: Namespace = Namespace("reservation", "reservation related endpoints")

reservation_model = namespace.model("Reservation", {
    "id": fields.Integer(
        readonly=True,
        description="Reservation id",
        required=False
    ),
    "confirmed": fields.Boolean(
        description="Is the reservation confirmed ?",
        required=True
    ),
    "canceled": fields.Boolean(
        description="Is the reservation canceled ?",
        required=True
    ),
    "idPassenger": fields.Integer(
        description="The passenger id",
        required=True
    ),
    "idClient": fields.Integer(
        description="The client id",
        required=True
    ),
    "idCompany": fields.Integer(
        description="The company id",
        required=True
    ),
    "idTrain": fields.Integer(
        description="The train id",
        required=True
    )
})


def convert_db_json(reservation: tuple) -> dict:
    return {
        "id": reservation[0],
        "confirmed": reservation[1],
        "canceled": reservation[2],
        "idPassenger": reservation[3],
        "idClient": reservation[4],
        "idCompany": reservation[5],
        "idTrain": reservation[6]
    }


@namespace.route("")
class ReservationGeneral(Resource):
    @namespace.marshal_list_with(reservation_model)
    @namespace.response(500, "Internal server error")
    def get(self) -> list:
        """Returns all the reservations"""
        reservations: list = request_database("SELECT * FROM Reservation")
        json_reservations: list = []
        for reservation in reservations:
            json_reservations.append(convert_db_json(reservation))
        return json_reservations

    @namespace.expect(reservation_model)
    def post(self):
        """Create a reservation"""
        json_data: json = request.json
        execute_database("INSERT INTO Reservation (Confirme, Annule, IdPassager, IdClient, IdCompanie, IdTrain)"
                         "VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(
            int(json_data["confirmed"]),
            int(json_data["canceled"]),
            json_data["idPassenger"],
            json_data["idClient"],
            json_data["idCompany"],
            json_data["idTrain"]
        ))


@namespace.route("/<int:id>")
@namespace.param("id", "the reservation id")
class Reservation(Resource):
    @namespace.marshal_with(reservation_model)
    @namespace.response(500, "BDD error")
    def get(self, id) -> dict:
        """Get reservation with specific id"""
        reservation: list = request_database("SELECT * from Reservation where Id={}".format(id))
        return reservation[0]

    def delete(self, id):
        """Delete company with specific id"""
        execute_database("DELETE FROM Reservation where Id={}".format(id))
