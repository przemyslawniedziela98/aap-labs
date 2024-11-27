from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask.logging import create_logger

db = SQLAlchemy()
migrate = Migrate()

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile("../instance/config.py", silent=True)

    db.init_app(app)
    migrate.init_app(app, db)

    logger = create_logger(app)
    app.logger = logger
    
    with app.app_context():
        from .models import user  
    from .routes.routes import auth_bp

    app.register_blueprint(auth_bp)

    return app
