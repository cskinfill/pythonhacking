import pytest
from app import app

@pytest.fixture
def client():
    app.config['TESTING'] = True 
    with app.test_client() as client:
        yield client

def test_homepage(client):
    response = client.get('/')
    assert response.status_code == 200
    assert b"Hello, World!" in response.data

def test_services(client):
    response = client.get('/services')
    assert response.status_code == 200
    data = response.get_json()
    assert len(data) == 2

def test_service1(client):
    response = client.get('/service/1')
    assert response.status_code == 200
    data = response.get_json()
    assert data["name"] == "Locate Us"