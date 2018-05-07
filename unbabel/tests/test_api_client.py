import pytest
import json
from app.api_client import APIClient


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
