import pytest
from app import create_app
from utils.extensions import db
from models.section import Section
from models.slider_image import SliderImage
from models.user import User
import os
import shutil

@pytest.fixture
def app():
    app = create_app('testing')

    # Configure a temporary upload folder for tests
    app.config['UPLOAD_FOLDER'] = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'test_uploads')
    if not os.path.exists(app.config['UPLOAD_FOLDER']):
        os.makedirs(app.config['UPLOAD_FOLDER'])

    with app.app_context():
        db.create_all()
        # Create admin user
        admin = User(username='admin', email='admin@example.com')
        admin.set_password('admin')
        db.session.add(admin)
        db.session.commit()
        yield app
        db.session.remove()
        db.drop_all()

    # Clean up test uploads
    if os.path.exists(app.config['UPLOAD_FOLDER']):
        shutil.rmtree(app.config['UPLOAD_FOLDER'])

@pytest.fixture
def client(app):
    return app.test_client()

def test_index_page(client):
    """Test that the index page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Village Seniors' in response.data

def test_admin_dashboard_access(client):
    """Test access to admin dashboard."""
    response = client.get('/admin/')
    assert response.status_code == 200
    assert b'Admin Dashboard' in response.data

def test_slider_image_crud(client, app):
    """Test creating and deleting slider images."""
    # Test Add
    with app.app_context():
        initial_count = SliderImage.query.count()

    # Simulate file upload
    from io import BytesIO
    data = {
        'image': (BytesIO(b'fake image content'), 'test.jpg'),
        'alt_text': 'Test Image',
        'order': 1
    }

    response = client.post('/admin/slider/add', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert response.status_code == 200
    # The message is encoded, let's decode response data to check string
    decoded_response = response.data.decode('utf-8')
    assert 'Slider image added successfully' in decoded_response

    with app.app_context():
        assert SliderImage.query.count() == initial_count + 1
        new_image = SliderImage.query.filter_by(alt_text='Test Image').first()
        assert new_image is not None
        image_id = new_image.id

    # Test Delete
    response = client.post(f'/admin/slider/delete/{image_id}', follow_redirects=True)
    assert response.status_code == 200
    decoded_response = response.data.decode('utf-8')
    assert 'Slider image deleted successfully' in decoded_response

    with app.app_context():
        assert SliderImage.query.count() == initial_count

def test_section_update(client, app):
    """Test updating a section image."""
    # Seed a section
    with app.app_context():
        section = Section(slug='test_section', title='Test Section', image_url='old.jpg')
        db.session.add(section)
        db.session.commit()
        section_id = section.id

    # Update Image
    from io import BytesIO
    data = {
        'image': (BytesIO(b'new image content'), 'new.jpg')
    }

    response = client.post(f'/admin/section/update/{section_id}', data=data, content_type='multipart/form-data', follow_redirects=True)
    assert response.status_code == 200
    decoded_response = response.data.decode('utf-8')
    assert 'Image updated successfully' in decoded_response

    with app.app_context():
        updated_section = Section.query.get(section_id)
        assert 'new.jpg' in updated_section.image_url
