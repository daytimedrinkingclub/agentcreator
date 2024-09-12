from flask import Flask
from flask_migrate import Migrate
from config import Config
from extensions import db
from routes.routes import main as main_blueprint

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    Migrate(app, db)

    # Import models here
    from models.models import Chat, Message

    # Register blueprints
    app.register_blueprint(main_blueprint)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0", port=3000, debug=True)