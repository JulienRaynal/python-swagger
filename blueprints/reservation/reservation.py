import json
from flask import request
from flask_restx import Namespace, Resource, fields
import requests

from blueprints.client.client import ClientCompany, ClientGeneral
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

reservation_ux_model = namespace.model("Reservation", {
    "id_client": fields.Integer(
        description="The client id",
        required=True
    ),
    "id_company": fields.Integer(
        description="The company id",
        required=True
    ),
    "id_train": fields.Integer(
        description="The train id",
        required=True
    ),
    "client_name": fields.String(
        description="The name of the client",
        required=True
    ),
    "client_surname": fields.String(
        description="The surname of the client",
        required=True
    ),
    "client_address": fields.String(
        description="The address of the client",
        required=True
    ),
    "client_phone": fields.String(
        description="The phone number of the client",
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
        reservation: list = request_database("SELECT * from Reservation where Id={}".format(id))[0]
        return {
            "id": reservation[0],
            "confirmed": reservation[1],
            "canceled": reservation[2],
            "idPassenger": reservation[3],
            "idClient": reservation[4],
            "idCompany": reservation[5],
            "idTrain": reservation[6]
        }

    def delete(self, id):
        """Delete company with specific id"""
        execute_database("DELETE FROM Reservation where Id={}".format(id))


@namespace.route("/train")
class ReservationTrain(Resource):
    @namespace.expect(reservation_ux_model)
    @namespace.marshal_with(reservation_model)
    @namespace.response(500, "BDD error")
    def put(self):
        """Create a reservation"""
        json_data: json = request.json
        id_companie = json_data.get("id_company"),
        id_client= json_data.get("id_client")
        client_company = ClientCompany()
        client_data: dict = client_company.get(json_data.get("id_client"), json_data.get("id_company"))
        if client_data.get("client_id") is None:
            execute_database("INSERT INTO Client (Nom, Prenom, Adresse, Telephone)"
                             "VALUES ('{}', '{}', '{}', '{}')".format(
                json_data["client_name"],
                json_data["client_surname"],
                json_data["client_address"],
                json_data["client_phone"]
            ))
            id_client = request_database("SELECT Id \
                                                        FROM Client \
                                                        WHERE Nom='{}' AND Prenom='{}' \
                                                        AND Adresse='{}' AND Telephone='{}';".format(
                json_data["client_name"],
                json_data["client_surname"],
                json_data["client_address"],
                json_data["client_phone"]
            ))[0]
        execute_database("INSERT INTO CC (IdCompanie, IdClient) VALUES ({}, {});".format(
            id_companie[0], id_client[0]
        ))
        execute_database("INSERT INTO Passager (Nom, Prenom) VALUES ('{}', '{}');".format(
            json_data["client_name"],
            json_data["client_surname"],
        ))
        id_passager = request_database("SELECT Id FROM Passager WHERE Nom='{}' AND Prenom='{}';".format(
            json_data["client_name"],
            json_data["client_surname"],
        ))[0]
        execute_database("INSERT INTO Reservation (Confirme, Annule, IdPassager, IdClient, IdCompanie, IdTrain) \
                         VALUES (0, 0, {}, {}, {}, {});".format(
            id_passager[0],
            id_client[0],
            id_companie[0],
            json_data.get("id_train")
        ))
        id = request_database("SELECT Id \
                                FROM Reservation \
                                WHERE IdPassager={} AND IdClient={} AND IdCompanie={} AND IdTrain={};".format(
            id_passager[0],
            id_client[0],
            id_companie[0],
            json_data.get("id_train")
        ))[0]
        reservation = Reservation()
        return reservation.get(id[0])
