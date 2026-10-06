from models.favourite_city import FavoriteCity


def test_add_favourite(
        logged_client,
        app):

    response = logged_client.get(
        "/favourites/add/Milano",
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():

        city = FavoriteCity.query.filter_by(
            city_name="Milano"
        ).first()

        assert city is not None


def test_delete_favourite(
        logged_client,
        app):

    logged_client.get(
        "/favourites/add/Milano"
    )

    with app.app_context():

        city = FavoriteCity.query.filter_by(
            city_name="Milano"
        ).first()

        assert city is not None

        city_id = city.id

    response = logged_client.get(
        f"/favourites/delete/{city_id}",
        follow_redirects=True
    )

    assert response.status_code == 200

    with app.app_context():

        city = FavoriteCity.query.filter_by(
            id=city_id
        ).first()

        assert city is None