import pytest
from app import create_app

@pytest.fixture
def client():
    app = create_app('testing')
    with app.test_client() as client:
        yield client

def test_home_page(client):
    """Test that the home page loads correctly."""
    response = client.get('/')
    assert response.status_code == 200
    assert b'Village Seniors MRE' in response.data

def test_static_files_linked(client):
    """Test that CSS and JS files are linked."""
    response = client.get('/')
    content = response.data.decode('utf-8')
    print(content) # Print content to debug
    # Check if CSS and JS are correctly linked
    assert 'css/style.css' in content
    assert 'js/script.js' in content

def test_slider_images_random(client):
    """Test that slider images are from section_X.jpg."""
    response = client.get('/')
    content = response.data.decode('utf-8')
    # Check if at least one section image is in the slider part
    assert 'img/section_' in content
