import pytest
from app.database_wrapper import DatabaseWrapper

@pytest.fixture(scope='session')
def db_wrapper():
    return DatabaseWrapper(database_name='test')

@pytest.fixture(autouse=True, scope='function')
def run_around_tests(db_wrapper):
    db_wrapper.client.drop_database('test')
    yield
    db_wrapper.client.drop_database('test')

def test_insert_multiple_translations(db_wrapper):
    translations = [{'uid': '1', 'text': 'test_1'}, {'uid': '2', 'text': 'test_2'}]
    result = db_wrapper.upsert_translations(translations)
    inserted_translation_1 = db_wrapper.db.translations.find_one({'uid': '1'})
    inserted_translation_2 = db_wrapper.db.translations.find_one({'uid': '2'})

    assert result.upserted_count == 2
    assert db_wrapper.db.translations.count() == 2
    assert inserted_translation_1['text'] == 'test_1'
    assert inserted_translation_2['text'] == 'test_2'

def test_update_multiple_translations(db_wrapper):
    '''Should update a document if it has same 'uid' instead of inserting new one'''

    translations = [{'uid': '1', 'status': 'new'}, {'uid': '2', 'status': 'new'}]
    db_wrapper.upsert_translations(translations)
    updated_translations = [{'uid': '1', 'status': 'completed'}, {'uid': '2', 'status': 'completed'}]
    result =  db_wrapper.upsert_translations(updated_translations)
    translation_1 = db_wrapper.db.translations.find_one({'uid': '1'})
    translation_2 = db_wrapper.db.translations.find_one({'uid': '2'})

    assert result.inserted_count == 0
    assert result.modified_count == 2
    assert db_wrapper.db.translations.count() == 2
    assert translation_1['status'] == 'completed'
    assert translation_2['status'] == 'completed'
