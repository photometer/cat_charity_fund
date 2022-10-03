from datetime import datetime

import pytest


@pytest.mark.parametrize(
    "invalid_name",
    [
        "",
        "lovechimichangasbutnunchakuisbetternunchakis4life" * 3,
        None,
    ],
)
def test_create_invalid_project_name(superuser_client, invalid_name):
    response = superuser_client.post(
        '/charity_project/',
        json={
            "name": invalid_name,
            "description": "Project_1",
            "full_amount": 5000,
        },
    )
    assert (
        response.status_code == 422
    ), "Creating projects with an empty name or with a name longer than 100 characters should be prohibited."


@pytest.mark.parametrize(
    'desc', [
        '',
        None,
    ]
)
def test_create_project_no_desc(superuser_client, desc):
    response = superuser_client.post(
        '/charity_project/',
        json={
            'name': 'Dead pool',
            'description': desc,
            'full_amount': 5000,
        },
    )
    assert (
        response.status_code == 422
    ), 'Creating projects with an empty description should be prohibited.'


@pytest.mark.parametrize('json', [
    {'invested_amount': 100},
    {'fully_invested': True},
    {'id': 5000},
])
def test_create_project_with_autofilling_fields(superuser_client, json):
    response = superuser_client.post(
        '/charity_project/',
        json=json
    )
    assert (
        response.status_code == 422
    ), 'Trying to pass values for autocomplete fields in a query should return a 422 error.'


@pytest.mark.parametrize(
    "invalid_full_amount",
    [
        -100,
        0.5,
        "test",
        0.0,
        '',
        None,
    ],
)
def test_create_invalid_full_amount_value(superuser_client, invalid_full_amount):
    response = superuser_client.post(
        "/charity_project/",
        json={
            "name": "Project_1",
            "description": "Project_1",
            "full_amount": invalid_full_amount,
        },
    )
    assert (
        response.status_code == 422
    ), 'The required amount (full_amount) for the project must be an integer and greater than 0.'


def test_get_charity_project(user_client, charity_project):
    response = user_client.get('/charity_project/')
    assert (
        response.status_code == 200
    ), "A GET request to the `/charity_project/` endpoint should return a status code of 200."
    assert isinstance(
        response.json(), list
    ), "A GET request to the `/charity_project/` endpoint must return an object of type `list."
    assert len(response.json()) == 1, (
        "With a correct POST request to the `/charity_project/` endpoint, an object is not created in the database. "
        "Check `CharityProject` model."
    )
    data = response.json()[0]
    keys = sorted(
        [
            "name",
            "description",
            "full_amount",
            "id",
            "invested_amount",
            "fully_invested",
            "create_date",
        ]
    )
    assert (
        sorted(list(data.keys())) == keys
    ), f"When making a GET request to the `/charity_project/` endpoint, the API response must contain `{keys}` keys."
    assert response.json() == [
        {
            "create_date": "2010-10-10T00:00:00",
            "description": "Huge fan of chimichangas. Wanna buy a lot",
            "full_amount": 1000000,
            "fully_invested": False,
            "id": 1,
            "invested_amount": 0,
            "name": "chimichangas4life",
        }
    ], "When making a GET request to the `/charity_project/` endpoint, the body of the API response is different than expected."


def test_get_all_charity_project(
    user_client, charity_project, charity_project_nunchaku
):
    response = user_client.get("/charity_project/")
    assert (
        response.status_code == 200
    ), "Requesting all projects should return status code 200."
    assert isinstance(
        response.json(), list
    ), "When requesting all projects, an object of type `list` must be returned"
    assert len(response.json()) == 2, (
        "With a correct POST request to the `/charity_project/` endpoint, an object is not created in the database. "
        "Check `CharityProject` model."
    )
    data = response.json()[0]
    keys = sorted(
        [
            "name",
            "description",
            "full_amount",
            "id",
            "invested_amount",
            "fully_invested",
            "create_date",
        ]
    )
    assert (
        sorted(list(data.keys())) == keys
    ), f"When requesting all projects, API presponse must contain `{keys}` keys."
    assert response.json() == [
        {
            "create_date": "2010-10-10T00:00:00",
            "description": "Huge fan of chimichangas. Wanna buy a lot",
            "full_amount": 1000000,
            "fully_invested": False,
            "id": 1,
            "invested_amount": 0,
            "name": "chimichangas4life",
        },
        {
            "create_date": "2010-10-10T00:00:00",
            "description": "Nunchaku is better",
            "full_amount": 5000000,
            "fully_invested": False,
            "id": 2,
            "invested_amount": 0,
            "name": "nunchaku",
        },
    ], "When requesting all projects, API response body is different from expected."


def test_create_charity_project(superuser_client):
    response = superuser_client.post(
        "/charity_project/",
        json={
            "name": "Dead pool",
            "description": "Deadpool inside",
            "full_amount": 1000000,
        },
    )
    assert (
        response.status_code == 200
    ), "When the project is created, the status code 200 should be returned."
    data = response.json()
    keys = sorted(
        [
            "name",
            "description",
            "full_amount",
            "create_date",
            "fully_invested",
            "id",
            "invested_amount",
        ]
    )
    assert (
        sorted(list(data.keys())) == keys
    ), f"When the project is created, API response must contain `{keys}` keys."
    data.pop("create_date")
    assert data == {
        "description": "Deadpool inside",
        "full_amount": 1000000,
        "fully_invested": False,
        "id": 1,
        "invested_amount": 0,
        "name": "Dead pool",
    }, "When the project is created, API pesponse body is different from expected."


@pytest.mark.parametrize(
    "json",
    [
        {
            "name": "Dead pool",
            "full_amount": "1000000",
        },
        {
            "description": "Deadpool inside",
            "full_amount": "1000000",
        },
        {
            "name": "Dead pool",
            "description": "Deadpool inside",
        },
        {
            "name": "Dead pool",
            "description": "Deadpool inside",
            "full_amount": "Donat",
        },
        {
            "name": "Dead pool",
            "description": "Deadpool inside",
            "full_amount": "",
        },
        {},
    ],
)
def test_create_charity_project_validation_error(json, superuser_client):
    response = superuser_client.post("/charity_project/", json=json)
    assert response.status_code == 422, (
        "If the project was created incorrectly, status code 422 should be returned."
    )
    data = response.json()
    assert (
        "detail" in data.keys()
    ), "If the project was created incorrectly, API response must contain `detail` key."


def test_delete_project_usual_user(user_client, charity_project):
    response = user_client.delete('/charity_project/1')
    assert response.status_code == 401, "Only superuser can delete project."


def test_delete_charity_project(superuser_client, charity_project):
    response = superuser_client.delete(f"/charity_project/{charity_project.id}")
    assert (
        response.status_code == 200
    ), "When deleting a project, status code 200 should be returned."
    data = response.json()
    keys = sorted(
        [
            "name",
            "description",
            "full_amount",
            "id",
            "invested_amount",
            "fully_invested",
            "create_date",
            "close_date",
        ]
    )
    assert (
        sorted(list(data.keys())) == keys
    ), f"When deleting a project, the API response must contain `{keys}` keys."
    assert data == {
        "name": "chimichangas4life",
        "description": "Huge fan of chimichangas. Wanna buy a lot",
        "full_amount": 1000000,
        "id": 1,
        "invested_amount": 0,
        "fully_invested": False,
        "create_date": "2010-10-10T00:00:00",
        "close_date": None,
    }, "When deleting a project, API response body is different than expected."


def test_delete_charity_project_invalid_id(superuser_client):
    response = superuser_client.delete("/charity_project/999a4")
    assert (
        response.status_code == 422
    ), "If the project is incorrectly deleted, status code 422 should be returned."
    data = response.json()
    assert (
        "detail" in data.keys()
    ), "If the project is incorrectly deleted, API response must contain the `detail` key."


@pytest.mark.parametrize(
    "json, expected_data",
    [
        (
            {"full_amount": 10},
            {
                "name": "chimichangas4life",
                "description": "Huge fan of chimichangas. Wanna buy a lot",
                "full_amount": 10,
                "id": 1,
                "invested_amount": 0,
                "fully_invested": False,
                "close_date": None,
                "create_date": "2010-10-10T00:00:00",
            },
        ),
        (
            {"name": "chimi"},
            {
                "name": "chimi",
                "description": "Huge fan of chimichangas. Wanna buy a lot",
                "full_amount": 1000000,
                "id": 1,
                "invested_amount": 0,
                "fully_invested": False,
                "close_date": None,
                "create_date": "2010-10-10T00:00:00",
            },
        ),
        (
            {"description": "Give me the money!"},
            {
                "name": "chimichangas4life",
                "description": "Give me the money!",
                "full_amount": 1000000,
                "id": 1,
                "invested_amount": 0,
                "fully_invested": False,
                "close_date": None,
                "create_date": "2010-10-10T00:00:00",
            },
        ),
    ],
)
def test_update_charity_project(superuser_client, charity_project, json, expected_data):
    response = superuser_client.patch("/charity_project/1", json=json)
    assert (
        response.status_code == 200
    ), "When the project is updated, status code 200 should be returned."
    data = response.json()
    keys = sorted(
        [
            "name",
            "description",
            "full_amount",
            "id",
            "invested_amount",
            "fully_invested",
            "create_date",
            "close_date",
        ]
    )
    assert (
        sorted(list(data.keys())) == keys
    ), f"When updating a project, the API response must contain `{keys}` keys."
    assert (
        data == expected_data
    ), "When updating the project, API response body is different than expected."


@pytest.mark.parametrize('json', [
    {'full_amount': 100},
    {'full_amount': 1000},
])
def test_update_charity_project_full_amount_equal_invested_amount(superuser_client, charity_project_little_invested, json):
    response = superuser_client.patch(
        '/charity_project/1',
        json=json,
    )
    assert (
        response.status_code == 200
    ), (
        'When editing a project, it should be allowed to set the required amount greater than or equal to the deposited amount.'
        'Status code 200 should be returned.'
    )
    assert response.json()['full_amount'] == json['full_amount'], (
        'When editing a project, it should be allowed to set the required amount greater than or equal to the deposited amount. '
        'Required amount has not changed.'
    )


@pytest.mark.parametrize(
    "json",
    [
        {"desctiption": ""},
        {"name": ""},
        {"full_amount": ""},
        {"invested_amount": 100},
        {"create_date": '2010-10-10'},
        {"close_date": '2010-10-10'},
        {"fully_invested": True},
    ],
)
def test_update_charity_project_invalid(superuser_client, charity_project, json):
    response = superuser_client.patch('/charity_project/1', json=json)
    assert response.status_code == 422, (
        'When editing a project, you cannot assign an empty name, description, or fund goal. '
        'Status code 422 should be returned.'
    )


def test_update_charity_project_same_name(superuser_client, charity_project, charity_project_nunchaku):
    response = superuser_client.patch(
        '/charity_project/1',
        json={
            'name': 'nunchaku',
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'full_amount': 1000000,
        },
    )
    assert response.status_code == 400, (
        'When editing a project, its new name must be unique.'
    )
    assert response.json() == {
        'detail': 'Project with the same name already exists!'
    }


@pytest.mark.parametrize('full_amount', [
    0,
    5,
])
def test_update_charity_project_full_amount_smaller_already_invested(superuser_client, charity_project_little_invested, full_amount):
    response = superuser_client.patch(
        '/charity_project/1',
        json={
            'name': 'nunchaku',
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'invested_amount': full_amount,
        },
    )
    assert response.status_code == 422, (
        'When editing a project, it should be prohibited to set the required amount less than the deposited amount.'
    )


def test_create_charity_project_usual_user(user_client):
    response = user_client.post(
        "/charity_project/",
        json={
            "name": "Dead pool",
            "description": "Deadpool inside",
            "full_amount": 1000000,
        },
    )
    assert (
        response.status_code == 401
    ), "If the project is created by a non-superuser, the status code 401 should be returned."
    data = response.json()
    assert (
        "detail" in data
    ), "If the project is created by a non-superuser, API response must contain `detail` key."
    assert data == {
        "detail": "Unauthorized",
    }, "When creating a project as a non-superuser, the body of the API response is different than expected."


def test_patch_charity_project_usual_user(user_client):
    response = user_client.patch("/charity_project/1", json={"full_amount": 10})
    assert (
        response.status_code == 401
    ), "If the project is updated by a non-superuser, the status code 401 should be returned."
    data = response.json()
    assert (
        "detail" in data
    ), "If the project is updated by a non-superuser, API response must contain `detail` key."
    assert data == {
        "detail": "Unauthorized",
    }, "When updating a project as a non-superuser, the body of the API response is different than expected."


def test_patch_charity_project_fully_invested(
    superuser_client, small_fully_charity_project,
):
    response = superuser_client.patch("/charity_project/1", json={"full_amount": 10})
    assert response.status_code == 400, (
        "When updating a project that has been fully invested, "
        "status code 400 should be returned."
    )
    data = response.json()
    assert "detail" in data, (
        "When updating a project that has been fully invested, "
        "response must contain `detail` key."
    )
    assert data == {"detail": "Closed project cannot be edited!", }, (
        "When updating a project that has been fully invested, "
        "API response body is different from expected."
    )


def test_create_charity_project_same_name(superuser_client, charity_project):
    response = superuser_client.post(
        "/charity_project/",
        json={
            'name': 'chimichangas4life',
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'full_amount': 1000000,
        },
    )
    assert response.status_code == 400, (
        "When creating a project with a non-unique name, "
        "status code 400 should be returned."
    )
    data = response.json()
    assert "detail" in data, (
        "When creating a project with a non-unique name, "
        "response must contain `detail` key."
    )
    assert data == {"detail": "Project with the same name already exists!"}, (
        "When creating a project with a non-unique name, "
        "API response body is different from expected."
    )


def test_create_charity_project_diff_time(superuser_client):
    response_chimichangs = superuser_client.post(
        "/charity_project/",
        json={
            'name': 'chimichangas4life',
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'full_amount': 1000000,
        },
    )
    response_nunchaku = superuser_client.post(
        "/charity_project/",
        json={
            'name': 'nunchaku',
            'description': 'Nunchaku is better',
            'full_amount': 5000000,
        },
    )
    chimichangas_create_date = response_chimichangs.json()['create_date']
    nunchakus_create_date = response_nunchaku.json()['create_date']
    assert chimichangas_create_date != nunchakus_create_date, (
        'When creating two projects in a row, the creation time does not differ. '
        'Check default value for `create_date` attribute.'
    )


def test_donation_exist_project_create(superuser_client, donation):
    response = superuser_client.post(
        "/charity_project/",
        json={
            "name": "Dead pool",
            "description": "Deadpool inside",
            "full_amount": 100,
        },
    )
    data = response.json()
    assert data['fully_invested'], (
        'If the new required amount is equal to the already invested amount, the project must be closed. '
        'In this case `fully_invested=True` should be set.'
    )
    assert data['close_date'] == datetime.now().strftime('%Y-%m-%dT%H:%M:%S'), (
        'If the new required amount is equal to the already invested amount, the project must be closed. '
        'In this case `close_date=<current time>` should be set.'
    )


def test_delete_charity_project_already_invested(superuser_client, charity_project_little_invested):
    response = superuser_client.delete('/charity_project/1')
    assert response.status_code == 400, (
        'Deleting projects that have already been funded should be prohibited. '
        'Response status code is different from expected.'
    )
    assert response.json()['detail'] == 'Funds have been contributed to the project, cannot be deleted!', (
        'Deleting projects that have already been funded should be prohibited. '
        'Response body is different from expected.'
    )


def test_delete_charity_project_already_closed(superuser_client, closed_charity_project):
    response = superuser_client.delete('/charity_project/1')
    assert response.status_code == 400, (
        'Deleting closed projects should be prohibited. '
        'Response status code is different from expected.'
    )
    assert response.json()['detail'] == 'Funds have been contributed to the project, cannot be deleted!', (
        'Deleting closed projects should be prohibited. '
        'Response body is different from expected.'
    )


def test_get_all_charity_project_not_auth_user(test_client, charity_project, charity_project_nunchaku):
    response = test_client.get("/charity_project/")
    assert response.status_code == 200, (
        'List of projects must be available even for an unauthorized user.'
    )
    data = response.json()
    assert data == [
        {
            'create_date': '2010-10-10T00:00:00',
            'description': 'Huge fan of chimichangas. Wanna buy a lot',
            'full_amount': 1000000,
            'fully_invested': False,
            'id': 1,
            'invested_amount': 0,
            'name': 'chimichangas4life'
        },
        {
            'create_date': '2010-10-10T00:00:00',
            'description': 'Nunchaku is better',
            'full_amount': 5000000,
            'fully_invested': False,
            'id': 2,
            'invested_amount': 0,
            'name': 'nunchaku'
        }
    ]
