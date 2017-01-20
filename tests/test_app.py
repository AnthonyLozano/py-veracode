from unittest.mock import MagicMock

import pytest

from veracode import Api, App

TEST_APP_ID = 284174
TEST_BUILD_ID = 1139745


@pytest.fixture
def app():
    api = Api(credential_file='test-credential')
    return App(TEST_APP_ID, api)


def test_retrieve_info(app):
    app.api.submit = MagicMock(return_value=open('data/app-info-response.xml'))
    app.retrieve_info()
