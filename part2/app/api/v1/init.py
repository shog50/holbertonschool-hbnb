from flask import Blueprint
from flask_restx import Api

api_v1 = Blueprint('api_v1', __name__, url_prefix='/api/v1')
api = Api(api_v1, version='1.0', title='My API', description='A simple API')

from .places import api as places_api
from .reviews import api as reviews_api

api.add_namespace(places_api)
api.add_namespace(reviews_api)
