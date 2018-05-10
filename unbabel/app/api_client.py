import os
import json
import requests
import concurrent.futures
import time
from database_wrapper import DatabaseWrapper

UNBABEL_API_BASE_URL = os.environ.get('UNBABEL_API_BASE_URL', 'https://sandbox.unbabel.com/tapi/v2')
TRANSLATION_URL = '{}/translation/'.format(UNBABEL_API_BASE_URL)
DEFAULT_LANGUAGE = 'en'

USERNAME = 'fullstack-challenge'
API_KEY = os.environ.get('UNBABEL_API_KEY', '9db71b322d43a6ac0f681784ebdcc6409bb83359')

HEADERS = {
    'Authorization': 'ApiKey {}:{}'.format(USERNAME, API_KEY),
    'Content-Type': 'application/json'
    }

class APIClient(object):

    def __init__(self, db_wrapper=DatabaseWrapper()):
        self.db_wrapper = db_wrapper

    def translate(self, texts, source_language=DEFAULT_LANGUAGE, target_languages=['pt', 'fr']):
        data = {'objects': []}
        for text in texts:
            for target_language in target_languages:
                new_object = {'text': text, 'source_language': source_language, 'target_language': target_language}
                data['objects'].append(new_object)

        response = requests.patch(TRANSLATION_URL, json.dumps(data), headers=HEADERS)
        return json.loads(response.content)

    def get_translation(self, uid):
        response = requests.get('{}{}'.format(TRANSLATION_URL, uid), headers=HEADERS)
        return json.loads(response.content)

    def get_translations(self, translation_uids):
        executor = concurrent.futures.ThreadPoolExecutor()
        future_results = [executor.submit(self.get_translation, uid) for uid in translation_uids]
        concurrent.futures.wait(future_results)
        return [future.result() for future in future_results]

    def update_translations_until_completed(self, translation_uids, max_wait_in_seconds=300, wait_time_between_updates=20):
        incomplete_translations_uids = translation_uids
        max_wait_time = time.time() + max_wait_in_seconds
        while (time.time() <= max_wait_time):
            translations = self.get_translations(incomplete_translations_uids)
            self.db_wrapper.upsert_translations(translations)
            for translation in translations:
                if translation['status'].lower() == 'completed':
                    incomplete_translations_uids.remove(translation['uid'])
            if len(incomplete_translations_uids) == 0: return
            time.sleep(wait_time_between_updates)
