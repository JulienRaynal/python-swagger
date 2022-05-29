import json
from flask import request
from flask_restx import Namespace, Resource, fields

from database.database import request_database, execute_database

namespace: Namespace = Namespace("company", "company related endpoints")

company_model = namespace.model("Company", {
    "id": fields.Integer(
        readonly=True,
        description="Company id",
        required=False
    ),
    "name": fields.String(
        description="Company name",
        required=True
    ),
    "canceled": fields.Boolean(
        description="as canceled the trains ?",
        required=True
    )
})


def convert_db_json(company: tuple) -> dict:
    return {
        "id": company[0],
        "name": company[1],
        "canceled": company[2]
    }


@namespace.route("")
class CompanyGeneral(Resource):
    @namespace.marshal_list_with(company_model)
    @namespace.response(500, "Internal server error")
    def get(self) -> list:
        """Returns all the companies"""
        companies: list = request_database("SELECT * FROM Companie")
        json_companies: list = []
        for company in companies:
            json_companies.append(convert_db_json(company))
        return json_companies

    @namespace.expect(company_model)
    def post(self):
        """Create a company"""
        json_data: json = request.json
        execute_database("INSERT INTO Companie (Nom, Annule)"
                         "VALUES ('{}', '{}')".format(
            json_data["name"],
            int(json_data["canceled"])
        ))


@namespace.route("/<int:id>")
@namespace.param("id", "the company id")
class Company(Resource):
    @namespace.marshal_with(company_model)
    @namespace.response(500, "BDD error")
    def get(self, id) -> dict:
        """Get company with specific id"""
        company: list = request_database("SELECT * from Companie where Id={}".format(id))
        return company[0]

    def delete(self, id):
        """Delete company with specific id"""
        execute_database("DELETE FROM Companie where Id={}".format(id))
