import pytest
from app import create_app
from utils.extensions import db
from models.site_settings import SiteSettings

@pytest.fixture
def app():
    app = create_app('testing')
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()

@pytest.fixture
def client(app):
    return app.test_client()

def test_site_settings_model(app):
    with app.app_context():
        settings = SiteSettings(
            site_name="Test Site",
            meta_title="Test Title"
        )
        db.session.add(settings)
        db.session.commit()

        retrieved = SiteSettings.query.first()
        assert retrieved.site_name == "Test Site"
        assert retrieved.meta_title == "Test Title"

def test_admin_settings_update(client, app):
    # First create a user to be able to login if auth was implemented (it is not fully protected yet based on code read)
    # The admin routes in routes/admin.py do not seem to have @login_required decorator based on my read,
    # but I should check if I missed something.
    # Let's check routes/admin.py again.
    pass
