import pytest
from ..api_client import APIClient

def test_get_top_stories_ids():
    """Checking that we get a list of integers"""
    top_stories_ids = APIClient().get_top_stories_ids()

    assert isinstance(top_stories_ids, list)
    assert all(isinstance(id, int) for id in top_stories_ids)

def test_get_top_stories():
    """Fetching N top stories"""
    top_stories = APIClient().get_top_stories(2)

    assert len(top_stories) == 2
    assert isinstance(top_stories[0], dict)
    assert isinstance(top_stories[1], dict)
    assert isinstance(top_stories[0]['title'], str)
    assert isinstance(top_stories[0]['score'], int)
    assert top_stories[0]['type'] == 'story'

def test_sort_stories_by_ranking():
    """Sorting stories from the most voted to the least voted"""
    stories = [{'score': 100}, {'score': 300}, {'score': 200}]
    stories_by_ranking = APIClient().sort_stories_by_ranking(stories)

    assert [story['score'] for story in stories_by_ranking] == [300, 200, 100]
