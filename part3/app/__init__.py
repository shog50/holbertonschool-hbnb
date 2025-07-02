from flask import Flask
from flask_jwt_extended import JWTManager

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    # Initialize JWT
    jwt = JWTManager(app)
    
    # Import and register blueprints/APIs
    from app.api.v1.auth import auth_bp
    app.register_blueprint(auth_bp)
    
    return app
