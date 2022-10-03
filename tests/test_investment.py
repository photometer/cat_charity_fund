import pytest


def test_donation_exist_non_project(superuser_client, donation):
    response_donation = superuser_client.get('/donation/')
    data_donation = response_donation.json()
    assert len(data_donation) == 1, (
        'If donation is received but no projects are open, the entire amount '
        'from the donation must be pending the opening of a new project.'
    )
    assert data_donation[0]['invested_amount'] == 0, (
        'If a donation is received but no projects are open, '
        'the invested_amount must remain zero.'
    )


def test_project_exist_non_donations(superuser_client, charity_project):
    response = superuser_client.get('/charity_project/')
    data = response.json()
    assert data[0]['invested_amount'] == 0, (
        'If there is a project but no donations yet, the invested_amount '
        'should remain zero.'
    )


def test_fully_invested_amount_for_two_projects(user_client, charity_project, charity_project_nunchaku):
    """
    Created 2 empty projects. Test creates 2 donations that fully cover
    the investments of the first project. The second project must remain
    uninvested.
    """
    user_client.post('/donation/', json={
        'full_amount': 500000,
    })
    user_client.post('/donation/', json={
        'full_amount': 500000,
    })
    assert charity_project.fully_invested, test_fully_invested_amount_for_two_projects.__doc__
    assert not charity_project_nunchaku.fully_invested, test_fully_invested_amount_for_two_projects.__doc__
    assert charity_project_nunchaku.invested_amount == 0, test_fully_invested_amount_for_two_projects.__doc__


def test_donation_to_little_invest_project(user_client, charity_project_little_invested, charity_project_nunchaku):
    """
    Created 2 projects, one of which is partially invested. Test creates
    a donation. Donations should be added to the first project, and the second
    will remain untouched.
    """
    user_client.post('/donation/', json={
        'full_amount': 900,
    })
    assert not charity_project_little_invested.fully_invested, test_donation_to_little_invest_project.__doc__
    assert charity_project_little_invested.invested_amount == 1000, test_donation_to_little_invest_project.__doc__
    assert not charity_project_nunchaku.fully_invested, test_donation_to_little_invest_project.__doc__
    assert charity_project_nunchaku.invested_amount == 0, test_donation_to_little_invest_project.__doc__
