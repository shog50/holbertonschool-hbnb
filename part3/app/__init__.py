from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_restx import Api

from config import DevelopmentConfig
from app.api.v1.auth import auth as auth_ns
from app.api.v1.users import ns as users_ns, ns_users as admin_users_ns
from app.api.v1.places import ns as places_ns
from app.api.v1.reviews import ns as reviews_ns

# Initialize extensions
db = SQLAlchemy()
bcrypt = Bcrypt()
jwt = JWTManager()

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

    # Register all API namespaces
    api = Api(app, version="1.0", title="HBnB API", prefix="/api/v1")

    api.add_namespace(auth_ns, path="/auth")                 # /api/v1/auth
    api.add_namespace(users_ns, path="/users")               # /api/v1/users
    api.add_namespace(admin_users_ns, path="/admin/users")   # /api/v1/admin/users
    api.add_namespace(places_ns, path="/places")             # optional
    api.add_namespace(reviews_ns, path="/reviews")           # optional

    print("Routes loaded:")
    print([str(rule) for rule in app.url_map.iter_rules()])
 
    return app
