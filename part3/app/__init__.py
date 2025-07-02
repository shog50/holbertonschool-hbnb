from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')
    
    db.init_app(app)
    
    with app.app_context():
        from models.base import BaseModel
        from models.user import User
        db.create_all()
        
        from services.facade import Facade
        app.facade = Facade(db.session)
    
    return app
