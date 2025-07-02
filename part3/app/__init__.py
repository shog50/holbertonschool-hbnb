from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize extensions
db = SQLAlchemy()

def create_app(config_name='default'):
    """Application factory function
    
    Args:
        config_name (str): Name of the configuration to use ('development', 'testing', etc.)
    
    Returns:
        Flask: The configured Flask application instance
    """
    app = Flask(__name__)
    
    # Apply configuration
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    # Import and register blueprints here to avoid circular imports
    from app.views import main_bp
    app.register_blueprint(main_bp)
    
    # Create database tables
    with app.app_context():
        db.create_all()
    
    return app
