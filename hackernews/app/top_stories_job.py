import dramatiq
from api_client import APIClient
from database_wrapper import DatabaseWrapper

@dramatiq.actor
def get_top_stories_with_comments():
    api_client = APIClient()
    db_wrapper = DatabaseWrapper()
    json_response = api_client.get_top_stories_with_comments()
    db_wrapper.upsert_stories(json_response['stories'])
    db_wrapper.upsert_comments(json_response['comments'])
