import dramatiq
from api_client import APIClient

@dramatiq.actor
def translate(texts):
    api_client = APIClient()
    json_response = api_client.translate(texts)
    translation_uids = [translation_object['uid'] for translation_object in json_response['objects']]
    api_client.update_translations_until_completed(translation_uids)
