from datetime import datetime

import pytest


@pytest.mark.parametrize('json, keys, expected_data', [
    (
        {'full_amount': 10},
        ['full_amount', 'id', 'create_date'],
        {'full_amount': 10, 'id': 1},
    ),
    (
        {'full_amount': 5, 'comment': 'To you for chimichangas'},
        ['full_amount', 'id', 'create_date', 'comment'],
        {'full_amount': 5, 'id': 1, 'comment': 'To you for chimichangas'},
    ),
])
def test_create_donation(user_client, json, keys, expected_data):
    response = user_client.post('/donation/', json=json)
    assert response.status_code == 200, (
        'When creating a donation, the status code 200 should be returned.'
    )
    data = response.json()
    assert sorted(list(data.keys())) == sorted(keys), (
        f'When creating a donation, response must contain `{keys}` keys.'
    )
    data.pop('create_date')
    assert data == expected_data, (
        'When creating a donation, API response body is different from expected.'
    )


@pytest.mark.parametrize('json', [
    {'comment': 'To you for chimichangas'},
    {'full_amount': -1},
    {'full_amount': None},
    {'fully_invested': True},
    {'user_id': 3},
    {'create_date': str(datetime.now())},
    {'invested_amount': 10},
])
def test_create_donation_incorrect(user_client, json):
    response = user_client.post('/donation/', json=json)
    assert response.status_code == 422, (
        'In case of incorrect POST request body to the `/donation/` endpoint '
        'status code 422 should be returned.'
    )


def test_get_user_donation(user_client, donation):
    response = user_client.get('/donation/my')
    assert response.status_code == 200, (
        'When receiving a list of user donations, the status code 200 should be returned.'
    )
    assert isinstance(response.json(), list), (
        'When receiving a list of user donations, an object of type `list` should be returned.'
    )
    assert len(response.json()) == 1, (
        'With a correct POST request to the `/charity_project/` endpoint, an object is not created in the database.'
        'Check `Donation` model.'
    )
    data = response.json()[0]
    keys = sorted([
        'full_amount',
        'comment',
        'id',
        'create_date',
    ])
    assert sorted(list(data.keys())) == keys, (
        f'When receiving a list of user donations, response should contain the `{keys}` keys.'
    )
    assert response.json() == [{
        'comment': 'To you for chimichangas',
        'create_date': '2011-11-11T00:00:00',
        'full_amount': 100,
        'id': 1,
    }], 'When receiving a list of user donations, API response body is different from expected.'


def test_get_all_donations(superuser_client, donation, another_donation):
    response = superuser_client.get('/donation/')
    assert response.status_code == 200, (
        'When receiving a list of all donations, status code 200 should be returned.'
    )
    assert isinstance(response.json(), list), (
        'When receiving a list of all donations, an object of type `list` should be returned.'
    )
    assert len(response.json()) == 2, (
        'With a correct POST request to the `/charity_project/` endpoint, an object is not created in the database. '
        'Check `Donation` model.'
    )
    data = response.json()[0]
    keys = sorted([
        'full_amount',
        'comment',
        'id',
        'create_date',
        'user_id',
        'invested_amount',
        'fully_invested',
    ])
    assert sorted(list(data.keys())) == keys, (
        f'When receiving a list of all donations, response must contain `{keys}` keys.'
    )
    data = response.json()
    assert data == [
        {
            'comment': 'To you for chimichangas',
            'create_date': '2011-11-11T00:00:00',
            'full_amount': 100,
            'id': 1,
            'user_id': 2,
            'invested_amount': 0,
            'fully_invested': False,
        },
        {
            'comment': 'From admin',
            'create_date': '2012-12-12T00:00:00',
            'full_amount': 2000,
            'id': 2,
            'user_id': 1,
            'invested_amount': 0,
            'fully_invested': False,
        }
    ], 'When receiving a list of all donations, API response body is different from expected.'


@pytest.mark.parametrize('json', [
    {'full_amount': -1},
    {'full_amount': 0.5},
    {'full_amount': 0.155555},
    {'full_amount': -1.5},
])
def test_donation_invalid(user_client, json):
    response = user_client.post('/donation/', json=json)
    assert response.status_code == 422, (
        'Donation amount must be an integer and greater than 0. '
        'Status code should be 422.'
    )


def test_donation_superuser_UD_enpoints(superuser_client, donation):
    response = superuser_client.patch('/donation/1')
    assert response.status_code == 404, (
        'Superuser cannot edit donations'
    )
    response = superuser_client.delete('/donation/1')
    assert response.status_code == 404, (
        'Superuser should be prevented from deleting donations'
    )


def test_donation_auth_user_UD_enpoints(user_client, donation):
    response = user_client.patch('/donation/1')
    assert response.status_code == 404, (
        'Registered user should not be allowed to edit donations'
    )
    response = user_client.delete('/donation/1')
    assert response.status_code == 404, (
        'Registered user should not be allowed to delete donations'
    )


def test_donation_user_UD_enpoints(test_client, donation):
    response = test_client.patch('/donation/1')
    assert response.status_code == 404, (
        'Unregistered user should not be allowed to edit donations'
    )
    response = test_client.delete('/donation/1')
    assert response.status_code == 404, (
        'Unregistered user should not be allowed to delete donations'
    )


def test_create_donation_check_create_date(user_client):
    response_1 = user_client.post('/donation/', json={'full_amount': 10})
    response_2 = user_client.post('/donation/', json={'full_amount': 20})
    assert response_1.json()['create_date'] != response_2.json()['create_date'], (
        'When creating 2 donations with a pause (of 1 second, for example), they must have different `create_date`'
    )
