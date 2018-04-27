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

def test_sort_stories_by_ranking():
    """Sorting stories from the most voted to the least voted"""
    stories = [{'score': 100}, {'score': 300}, {'score': 200}]
    stories_by_ranking = APIClient().sort_stories_by_ranking(stories)

    assert [story['score'] for story in stories_by_ranking] == [300, 200, 100]

def test_get_all_comments():
    """Retrieves all the comments belonging to a story"""

    # the story will have 3 descendants in total
    def get_item(*args):
        if args[0] == 2:
            return {'id': 2}
        elif args[0] == 3:
            return {'id': 3, 'kids': [4]}
        elif args[0] == 4:
            return {'id': 4}

    api_client = APIClient()
    api_client.get_item = Mock(side_effect=get_item)
    story = {'id': 1, 'kids': [2, 3]}
    comments = api_client.get_all_comments(story)
    comment_ids = [comment['id'] for comment in comments]
    comment_ids.sort()

    assert comment_ids == [2, 3, 4]
