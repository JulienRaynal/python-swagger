import json

from flask import request
from flask_restx import Namespace, Resource, fields

from database.database import request_database, execute_database

namespace: Namespace = Namespace("client", "client related endpoints")

client_model = namespace.model("Client", {
    "id": fields.Integer(
        readonly=True,
        description="Client id",
        required=False
    ),
    "name": fields.String(
        description="Client name",
        required=True
    ),
    "surname": fields.String(
        description="Client surname",
        required=True
    ),
    "address": fields.String(
        description="Client living address",
        required=True
    ),
    "phone": fields.String(
        description="Client phone number",
        required=True
    )
})

client_company_model = namespace.model("Client in a company", {
    "company_id": fields.Integer(
        readonly=True,
        description="Company id"
    ),
    "company_name": fields.String(
        readonly=True,
        description="Company id"
    ),
    "client_id": fields.Integer(
        readonly=True,
        description="Client id"
    ),
    "client_name": fields.String(
        readonly=True,
        description="Client name"
    )
})

client_info = namespace.model("Info to find a client", {
    "id_client": fields.Integer(
        required=True,
        description="The client id"
    ),
    "id_company": fields.Integer(
        required=True,
        description="The company id"
    )
})


def convert_db_json(client: tuple) -> dict:
    return {
        "id": client[0],
        "name": client[1],
        "surname": client[2],
        "address": client[3],
        "phone": client[4]
    }


@namespace.route('')
class ClientGeneral(Resource):

    @namespace.marshal_list_with(client_model)
    @namespace.response(500, "Internal server error")
    def get(self) -> list:
        """Returns all the clients"""
        clients: list = request_database("SELECT * from Client")
        json_clients: list = []
        for client in clients:
            json_clients.append(convert_db_json(client))
        return json_clients

    @namespace.expect(client_model)
    def put(self):
        """Create user"""
        json_data = request.json
        execute_database("INSERT INTO Client (Nom, Prenom, Adresse, Telephone)"
                         "VALUES ('{}', '{}', '{}', '{}')".format(
            json_data["name"],
            json_data["surname"],
            json_data["address"],
            json_data["phone"]
        ))


@namespace.route("/<int:id>")
@namespace.param("id", "the client id")
class Client(Resource):
    @namespace.marshal_list_with(client_model)
    @namespace.response(500, "BDD error")
    def get(self, id) -> dict:
        """Get user with specific id"""
        client: list = request_database("SELECT * from Client where Id={}".format(id))
        return client[0]

    def delete(self, id):
        """Delete user with specific id"""
        execute_database("DELETE FROM Client where Id={}".format(id))


@namespace.route("/company/<int:clid>&<int:coid>")
@namespace.param("clid", "the client id")
@namespace.param("coid", "the company id")
class ClientCompany(Resource):
    @namespace.marshal_with(client_company_model)
    @namespace.response(500, "BDD error")
    def get(self, clid, coid) -> dict:
        """Check if user exists in specific company"""
        client: list = request_database("SELECt C.Id, C.Nom, C2.Id, C2.Nom \
                                            FROM CC \
                                            JOIN Companie C on CC.IdCompanie = C.Id \
                                            JOIN Client C2 on CC.IdClient = C2.Id \
                                            WHERE IdCompanie={} AND C2.Id={};".format(
            coid,
            clid
        ))
        client_data: dict = {}
        try:
            client_data = {
            "company_id": client[0][0],
            "company_name": client[0][1],
            "client_id": client[0][2],
            "client_name": client[0][3]
        }
        except Exception as e:
            print("no such data available")
        return client_data
