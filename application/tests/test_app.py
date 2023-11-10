import pytest
from Examensuppgift_python2.application.app import app


def test_index_route():

    # Skapar en testklient för Flaskapplicationen, kör appen utan att starta servern.

    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200


def test_form_route():

    # testar samma sak men våran form.html

    with app.test_client() as client:
        response = client.get('/form')
        assert response.status_code == 200


def test_api_post_valid_date():

    # Testar våra datum parametrar och ser ifall dom är giltiga.

    with app.test_client() as client:
        params = {'year': '2023', 'month': '11', 'day': '09', 'price_range': 'SE3'}
        try:
            response = client.post('/api', data=params)
            assert response.status_code == 200
        except ConnectionError:
            pytest.fail("Failed to connect to the URL")

def test_api_post_invalid_date():

    # Skapar en klient för att testa olika routes.
    # Skapa en dictionary med felinmatning för att få fel förfrågan
    # kolla att statuskoden inte är 200 då det är fel inmatning

    with app.test_client() as client:
        params = {'year': '2025', 'month': '13', 'day': '35', 'price_range': 'SE3'}
        try:
            response = client.post('/api', data=params)
            assert response.status_code != 200
        except ConnectionError:
            pytest.fail("Misslyckades med att ansluta till URL:en")


if __name__ == '__main__':
    pytest.main()