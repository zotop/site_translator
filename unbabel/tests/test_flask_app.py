import pytest
import json
import mock
from flask_app import app

@pytest.fixture(scope='session')
def test_client():
    return app.test_client()

@mock.patch('database_wrapper.DatabaseWrapper.get_translations')
def test_translations_status(mock_method, test_client):
    '''GET /api/translations/status should return json'''

    mock_translation = {'source_language': 'en', 'status': 'completed',
                        'target_language': 'pt', 'text': 'highway',
                        'uid': 'c8f86b5564'}
    mock_method.return_value = [mock_translation]

    response = test_client.get('/api/translations/status')
    json_response = json.loads(response.get_data())

    assert len(json_response) == 1
    assert response.status_code == 200
    assert response.mimetype == 'application/json'
    assert json_response[0]['uid']  == 'c8f86b5564'
    assert(set(mock_translation.keys()) == set(json_response[0].keys()))
