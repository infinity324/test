import pytest
from main import app, User, db


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
        yield client
        with app.app_context():
            db.drop_all()


def test_home_page(client):
    response = client.get('/')
    assert response.status_code == 200


def test_login_success(client):
    user = User(username='testuser', password='testpass')
    db.session.add(user)
    db.session.commit()
    response = client.post(
        '/login', data={'username': 'testuser', 'password': 'testpass'}, follow_redirects=True)
    assert b'登录成功！' in response.data


def test_login_failure(client):
    response = client.post(
        '/login', data={'username': 'wronguser', 'password': 'wrongpass'}, follow_redirects=True)
    assert b'登录失败，请检查用户名和密码。' in response.data
