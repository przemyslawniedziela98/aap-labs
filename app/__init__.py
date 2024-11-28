from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.logging import create_logger
from flask_login import LoginManager


db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    """
    Create and configure the Flask application.
    """
    app = Flask(__name__)
    app.config.from_pyfile("../instance/config.py", silent=True)

    db.init_app(app)
    migrate.init_app(app, db)

    logger = create_logger(app)
    app.logger = logger

    login_manager.init_app(app)
    login_manager.login_view = 'auth.login' 
    login_manager.login_message = "Please log in to access this page."
    login_manager.login_message_category = "info"

    @login_manager.user_loader
    def load_user(user_id: str):
        """
        Callback function for loading a user by ID.
        """
        from .models.user import User  
        return User.query.get(int(user_id))

    with app.app_context():
        from .models import user  
        from .routes.routes import auth_bp

        app.register_blueprint(auth_bp)

    return app
