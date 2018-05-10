import pytest
import json
from mock import Mock
from app.api_client import APIClient
from app.database_wrapper import DatabaseWrapper

@pytest.fixture(scope='session')
def db_wrapper():
    return DatabaseWrapper(database_name = 'test_db')

@pytest.fixture(autouse=True, scope='function')
def run_around_tests(db_wrapper):
    yield
    db_wrapper.client.drop_database('test_db')


def test_translate():
    """Checking that we can request translation of multiple texts at once"""
    texts = ['hello', 'world']
    response = APIClient().translate(texts, source_language='en', target_languages=['pt', 'fr'])
    json_response = json.loads(response.content)
    objects = json_response['objects']

    assert response.status_code == 202
    assert len(objects) == 4
    assert set([obj['source_language'] for obj in objects]) == {'en'}
    assert set(([obj['text'] for obj in objects])) == set(['world', 'hello'])
    assert set(([obj['target_language'] for obj in objects])) == set(['fr', 'pt'])

def test_get_translation():
    """Retrieving translation by uid"""
    response = APIClient().translate(['hello'], source_language='en', target_languages=['fr'])
    json_response = json.loads(response.content)
    translation_request = json_response['objects'][0]
    response = APIClient().get_translation(translation_request['uid'])
    json_response = json.loads(response.content)

    assert response.status_code == 200
    assert json_response['uid'] == translation_request['uid']
    assert json_response['text'] == translation_request['text']
    assert json_response['source_language'] == translation_request['source_language']
    assert json_response['target_language'] == translation_request['target_language']

def test_update_tranlations_until_completed(db_wrapper):
    """fetching and persisting translations until their status becomes 'completed' """
    api_client = APIClient(db_wrapper)
    mock_get_translations = []
    mock_get_translations.append([{'uid': 'fake_uid', 'status': 'new'}])
    mock_get_translations.append([{'uid': 'fake_uid', 'status': 'completed'}])
    api_client.get_translations = Mock(side_effect=mock_get_translations)
    api_client.update_tranlations_until_completed(translation_uids=['fake_uid'], wait_time_between_updates=0)
    translation = db_wrapper.db.translations.find_one()

    assert db_wrapper.db.translations.count() == 1
    assert translation['uid'] == 'fake_uid'
    assert translation['status'] == 'completed'
