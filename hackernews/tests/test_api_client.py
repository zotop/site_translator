import pytest
import json
from mock import Mock
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

def test_get_kids():
    """Retrieves kids of an item"""

    # the story will have 2 descendants in total
    def get_item(*args):
        if args[0] == 2:
            return {'id': 2}
        elif args[0] == 3:
            return {'id': 3}

    api_client = APIClient()
    api_client.get_item = Mock(side_effect=get_item)
    story = {'id': 1, 'kids': [2, 3]}
    comments = api_client.get_kids(story)
    comment_ids = [comment['id'] for comment in comments]
    comment_ids.sort()

    assert comment_ids == [2, 3]

def test_get_top_stories_with_comments():
    """Retrieves the top stories with all its direct kids/comments"""

    def get_top_stories(*args):
        return [{'id': 1, 'kids': [2]}, {'id': 3, 'kids': [4, 5]}]

    def get_kids(*args):
        if args[0] == {'id': 1, 'kids': [2]}:
            return [{'id': 2}]
        elif args[0] == {'id': 3, 'kids': [4, 5]}:
            return [{'id': 4}, {'id': 5}]

    api_client = APIClient()
    api_client.get_top_stories = Mock(side_effect=get_top_stories)
    api_client.get_kids = Mock(side_effect=get_kids)
    items = api_client.get_top_stories_with_comments(2) # get two top stories
    item_ids = [item['id'] for item in items]
    item_ids.sort()

    assert item_ids == [1, 2, 3, 4, 5]
