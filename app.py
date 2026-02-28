import os
from flask import Flask, render_template
from flask_caching import Cache
from config.config import config
from utils.extensions import db, migrate

# Initialize Cache using FileSystemCache to support multiple workers
cache_dir = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'cache')
cache = Cache(config={
    'CACHE_TYPE': 'FileSystemCache',
    'CACHE_DIR': cache_dir,
    'CACHE_DEFAULT_TIMEOUT': 300
})

def create_app(config_name=None):
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'default')

    app = Flask(__name__, template_folder='templates', static_folder='statics')
    app.config.from_object(config[config_name])

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)

    # Needs a secret key for session/flashing
    if not app.config.get('SECRET_KEY'):
        app.config['SECRET_KEY'] = 'dev-key-for-testing'

    # Register Blueprints
    from routes.main import main_bp
    app.register_blueprint(main_bp)

    from routes.admin import admin_bp
    app.register_blueprint(admin_bp)

    # Error Handlers
    @app.errorhandler(400)
    def bad_request(e):
        return render_template('error.html', error_code=400, error_message="Mauvaise requête"), 400

    @app.errorhandler(401)
    def unauthorized(e):
        return render_template('error.html', error_code=401, error_message="Non autorisé"), 401

    @app.errorhandler(403)
    def forbidden(e):
        return render_template('error.html', error_code=403, error_message="Accès interdit"), 403

    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('error.html', error_code=404, error_message="Page non trouvée"), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('error.html', error_code=500, error_message="Erreur interne du serveur"), 500

    # Context Processor for Site Settings
    from models.site_settings import SiteSettings

    @app.context_processor
    def inject_site_settings():
        site_settings = cache.get('site_settings')
        if site_settings is None:
            try:
                site_settings = SiteSettings.query.first()
            except:
                site_settings = None

            if not site_settings:
                site_settings = SiteSettings() # Ensure it's never None

            cache.set('site_settings', site_settings)

        return dict(site_settings=site_settings)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run()
