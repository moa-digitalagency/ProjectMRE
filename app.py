import os
from flask import Flask
from config.config import config
from utils.extensions import db, migrate

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')

    app = Flask(__name__, template_folder='templates', static_folder='statics')
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Needs a secret key for session/flashing
    if not app.config.get('SECRET_KEY'):
        app.config['SECRET_KEY'] = 'dev-key-for-testing'

    # Register Blueprints
    from routes.main import main_bp
    app.register_blueprint(main_bp)

    from routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    # Context Processor for Site Settings
    from models.site_settings import SiteSettings
    @app.context_processor
    def inject_site_settings():
        try:
            site_settings = SiteSettings.query.first()
        except:
            site_settings = None
        return dict(site_settings=site_settings)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
