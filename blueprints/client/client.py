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

client_example = {"id": 1,
                  "name": "Raynal",
                  "surname": "Julien",
                  "address": "30 rue des etudes",
                  "phone": "0666666666"}


# create_user_data = namespace.model(
#     "Insert user in database",
#     {"name": fields.String(description="client name", required=True),
#      "surname": fields.String(description="client surname", required=True),
#      "address": fields.String(description="client address", required=True),
#      "phone": fields.String(description="client phone number", required=True)
#      }
# )

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
    def post(self):
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
