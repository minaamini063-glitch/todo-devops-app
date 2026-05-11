import pytest
from app import create_app, db
from app.models import Todo

@pytest.fixture
def client():
    app = create_app()

    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'

    with app.test_client() as client:
        with app.app_context():
            db.create_all()

        yield client

        with app.app_context():
            db.drop_all()

def test_index_page(client):
    response = client.get('/')
    assert response.status_code == 200

def test_add_todo(client):
    response = client.post('/add', data={
        'title': 'Test Todo',
        'description': 'Test Description'
    })

    assert response.status_code == 302

def test_api_todos(client):
    response = client.get('/api/todos')
    assert response.status_code == 200

def test_complete_todo(client):
    client.post('/add', data={'title': 'Test Todo'})

    response = client.get('/complete/1')
    assert response.status_code == 302