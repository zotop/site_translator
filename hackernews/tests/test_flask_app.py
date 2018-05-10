import pytest
import json
import mock
from flask_app import app

@pytest.fixture(scope='session')
def test_client():
    return app.test_client()

@mock.patch('api_client.APIClient.get_top_stories_with_comments')
def test_get_top_stories_with_comments(mock_method, test_client):
    '''GET /top_stories/<int:number_of_stories> should return json'''

    mock_stories = [{'id': 1, 'type': 'story', 'kids': [2]}]
    mock_comments = [{'id': 2, 'type': 'comment'}]
    mock_method.return_value = {'stories': mock_stories, 'comments': mock_comments}
    response = test_client.get('/top_stories/1')
    json_response = json.loads(response.get_data())

    assert response.status_code == 200
    assert response.mimetype == 'application/json'
    assert json_response['stories']  == mock_stories
    assert json_response['comments'] == mock_comments
