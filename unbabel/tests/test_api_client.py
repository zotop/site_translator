import pytest
import json
from app.api_client import APIClient


def test_translate():
    """Checking that we can request translation of multiple texts at once"""
    texts = ['hello', 'world']
    response = APIClient().translate(texts, source_language='en', target_languages=['pt', 'fr'])
    json_response = json.loads(response.content)
    objects = json_response['objects']
    print(objects)
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
