from server import create_app, load_clubs, load_comps

import pytest


@pytest.fixture
def client():
    app = create_app({'TESTING': True})
    with app.test_client() as client:
        yield client


@pytest.fixture
def test_club():
    return load_clubs('tests/dataset.json')[0]


@pytest.fixture
def test_competition():
    return load_comps('tests/dataset.json')[0]
