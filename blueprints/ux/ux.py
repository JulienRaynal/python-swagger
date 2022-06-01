import json
from flask import request

from flask_restx import Namespace, Resource

from blueprints.client.client import ClientCompany
from blueprints.gare.gare import StationTrains, station_train_model
from blueprints.reservation.reservation import reservation_ux_model, reservation_model, ReservationTrain, Reservation
from blueprints.ville.ville import city_model, CityGeneral, CityStations, gare_from_city_model
from database.database import execute_database, request_database

namespace: Namespace = Namespace("ux", "full ux requests")


@namespace.route('/cities')
class UxGeneralCities(Resource):
    @namespace.marshal_list_with(city_model)
    @namespace.response(500, "Internal server error")
    def get(self):
        """list all cities"""
        city = CityGeneral()
        return city.get()


@namespace.route("/stations/<int:id>")
@namespace.param("id", "the city id")
class UxGeneralStations(Resource):
    @namespace.marshal_list_with(gare_from_city_model)
    @namespace.response(500, "Internal server error")
    def get(self, id):
        """list all the stations from a city"""
        city_stations = CityStations()
        return city_stations.get(id)


@namespace.route("/trains/<int:id>")
@namespace.param("id", "the station id")
class UxGeneralTrains(Resource):
    @namespace.marshal_list_with(station_train_model)
    @namespace.response(500, "Internal server error")
    def get(self, id):
        """list all the trains for a given station"""
        station_trains = StationTrains()
        return station_trains.get(id)

    @namespace.expect(reservation_ux_model)
    @namespace.marshal_with(reservation_model)
    @namespace.response(500, "BDD error")
    def put(self, id):
        """Create a reservation"""
        json_data: json = request.json
        id_companie = json_data.get("id_company"),
        id_client = json_data.get("id_client")
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
        execute_database("INSERT INTO CC (IdCompanie, IdClient) VALUES ({}, {});".format(
            id_companie[0], id_client
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
            id_client,
            id_companie[0],
            json_data.get("id_train")
        ))
        id = request_database("SELECT Id \
                                        FROM Reservation \
                                        WHERE IdPassager={} AND IdClient={} AND IdCompanie={} AND IdTrain={};".format(
            id_passager[0],
            id_client,
            id_companie[0],
            json_data.get("id_train")
        ))[0]
        reservation = Reservation()
        return reservation.get(id[0])

