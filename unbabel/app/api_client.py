import os
import json
import requests

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

    def translate(self, texts, source_language=DEFAULT_LANGUAGE, target_languages=['pt', 'fr']):
        data = {'objects': []}
        for text in texts:
            for target_language in target_languages:
                new_object = {'text': text, 'source_language': source_language, 'target_language': target_language}
                data['objects'].append(new_object)

        return requests.patch(TRANSLATION_URL, json.dumps(data), headers=HEADERS)

    def get_translation(self, uid):
        return requests.get('{}{}'.format(TRANSLATION_URL, uid), headers=HEADERS)
