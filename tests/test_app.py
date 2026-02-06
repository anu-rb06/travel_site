import sys
import os
import pytest

# Add project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    return app.test_client()

def test_home_page(client):
    response = client.get("/")
    assert response.status_code == 200

def test_register_page(client):
    response = client.get("/register")
    assert response.status_code == 200

def test_login_page(client):
    response = client.get("/login")
    assert response.status_code == 200

def test_packages_page(client):
    response = client.get("/packages")
    assert response.status_code == 200

