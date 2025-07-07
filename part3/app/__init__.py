from flask import Flask
from flask_restx import Api
from config import DevelopmentConfig
from app.extensions import db, bcrypt, jwt

def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)

   
    from app.api.v1.auth import auth as auth_ns
    from app.api.v1.users import ns as users_ns, ns_users as admin_users_ns
    from app.api.v1.places import ns as places_ns
    from app.api.v1.reviews import ns as reviews_ns

    # Register all API namespaces
    api = Api(app, version="1.0", title="HBnB API", prefix="/api/v1")
    api.add_namespace(auth_ns, path="/auth")
    api.add_namespace(users_ns, path="/users")
    api.add_namespace(admin_users_ns, path="/admin/users")
    api.add_namespace(places_ns, path="/places")
    api.add_namespace(reviews_ns, path="/reviews")

    print("Routes loaded:")
    print([str(rule) for rule in app.url_map.iter_rules()])

    return app
