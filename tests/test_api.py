import pytest 
import requests 

BASE_URL = 'http://web:5000' # User internal Docker service name

def test_register():
    response = requests.post(f'{BASE_URL}/api/register', json={
        'username': 'testuser',
        'password': 'testpass',
        'role': 'customer'
    })
    assert response.status_code == 200
    assert response.json()['success'] == True 

def test_login():
    response = requests.post(f'{BASE_URL}/api/login', json={
        'username': 'testuser',
        'password': 'testpass'
    })
    assert response.status_code == 200
    assert response.json()['success'] == True 

def test_get_products():
    response = requests.get(f'{BASE_URL}/api/products')
    assert response.status_code == 200
    assert isinstance(response.json(), list)