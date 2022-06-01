from flask import Blueprint
from flask_restx import Api

from blueprints.client.client import namespace as user_ns
from blueprints.train.train import namespace as train_ns
from blueprints.arret.arret import namespace as arret_ns
from blueprints.passenger.passenger import namespace as passenger_ns
from blueprints.ville.ville import namespace as city_ns
from blueprints.gare.gare import namespace as station_ns
from blueprints.companie.companie import namespace as company_ns
from blueprints.reservation.reservation import namespace as reservation_ns
from blueprints.ux.ux import namespace as ux_ns

blueprint: Blueprint = Blueprint("documented API", __name__, url_prefix="/")

api_extension: Api = Api(
    blueprint,
    title="Flask API demo",
    version="1.0",
    description="API to demonstrate REST and Swagger knowledge",
    doc="/doc"
)

api_extension.add_namespace(city_ns)
api_extension.add_namespace(station_ns)
api_extension.add_namespace(company_ns)
api_extension.add_namespace(train_ns)
api_extension.add_namespace(arret_ns)
api_extension.add_namespace(passenger_ns)
api_extension.add_namespace(user_ns)
api_extension.add_namespace(reservation_ns)
api_extension.add_namespace(ux_ns)