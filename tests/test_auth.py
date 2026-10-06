def test_register(client):

    response = client.post(
        "/auth/register",
        data={
            "username": "utente_test",
            "email": "utente@test.it",
            "password": "123456"
        },
        follow_redirects=True
    )

    assert response.status_code == 200


def test_login(client):

    client.post(
        "/auth/register",
        data={
            "username": "mario",
            "email": "mario@test.it",
            "password": "123456"
        }
    )

    response = client.post(
        "/auth/login",
        data={
            "username": "mario",
            "password": "123456"
        },
        follow_redirects=True
    )

    assert response.status_code == 200