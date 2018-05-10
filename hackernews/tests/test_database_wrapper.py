import pytest
from database_wrapper import DatabaseWrapper

@pytest.fixture(scope='session')
def db_wrapper():
    return DatabaseWrapper(database_name = 'test')

@pytest.fixture(autouse=True, scope='function')
def run_around_tests(db_wrapper):
    yield
    db_wrapper.client.drop_database('test')


def test_insert_one_story(db_wrapper):
    result = db_wrapper.upsert_stories([{'id': 13, 'title': 'test'}])
    inserted_story = db_wrapper.db.stories.find()[0]

    assert result.upserted_count == 1
    assert db_wrapper.db.stories.count() == 1
    assert inserted_story['id'] == 13
    assert inserted_story['title'] == 'test'

def test_insert_multiple_stories(db_wrapper):
    stories = [{'id': 1, 'title': 'test_1'}, {'id': 2, 'title': 'test_2'}]
    result = db_wrapper.upsert_stories(stories)
    inserted_story_1 = db_wrapper.db.stories.find_one({'id': 1})
    inserted_story_2 = db_wrapper.db.stories.find_one({'id': 2})

    assert result.upserted_count == 2
    assert db_wrapper.db.stories.count() == 2
    assert inserted_story_1['title'] == 'test_1'
    assert inserted_story_2['title'] == 'test_2'

def test_update_multiple_stories(db_wrapper):
    '''Should update a document if it has same 'id' instead of inserting new one'''

    stories = [{'id': 1, 'title': 'test_1'}, {'id': 2, 'title': 'test_2'}]
    db_wrapper.upsert_stories(stories)
    updated_stories = [{'id': 1, 'title': 'test_3'}, {'id': 2, 'title': 'test_4'}]
    result =  db_wrapper.upsert_stories(updated_stories)
    story_1 = db_wrapper.db.stories.find_one({'id': 1})
    story_2 = db_wrapper.db.stories.find_one({'id': 2})

    assert result.inserted_count == 0
    assert result.modified_count == 2
    assert db_wrapper.db.stories.count() == 2
    assert story_1['title'] == 'test_3'
    assert story_2['title'] == 'test_4'

def test_insert_one_comment(db_wrapper):
    result = db_wrapper.upsert_comments([{'id': 13, 'text': 'test'}])
    comment = db_wrapper.db.comments.find()[0]

    assert result.upserted_count == 1
    assert db_wrapper.db.comments.count() == 1
    assert comment['id'] == 13
    assert comment['text'] == 'test'

def test_insert_multiple_comments(db_wrapper):
    comments = [{'id': 1, 'text': 'test_1'}, {'id': 2, 'text': 'test_2'}]
    result = db_wrapper.upsert_comments(comments)
    comment_1 = db_wrapper.db.comments.find_one({'id': 1})
    comment_2 = db_wrapper.db.comments.find_one({'id': 2})

    assert result.upserted_count == 2
    assert db_wrapper.db.comments.count() == 2
    assert comment_1['text'] == 'test_1'
    assert comment_2['text'] == 'test_2'

def test_update_multiple_comments(db_wrapper):
    '''Should update a document if it has same 'id' instead of inserting new one'''

    comments = [{'id': 1, 'text': 'test_1'}, {'id': 2, 'text': 'test_2'}]
    db_wrapper.upsert_comments(comments)
    updated_comments = [{'id': 1, 'text': 'test_3'}, {'id': 2, 'text': 'test_4'}]
    result =  db_wrapper.upsert_comments(updated_comments)
    comment_1 = db_wrapper.db.comments.find_one({'id': 1})
    comment_2 = db_wrapper.db.comments.find_one({'id': 2})

    assert result.inserted_count == 0
    assert result.modified_count == 2
    assert db_wrapper.db.comments.count() == 2
    assert comment_1['text'] == 'test_3'
    assert comment_2['text'] == 'test_4'
