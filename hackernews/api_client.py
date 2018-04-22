import os
import requests
import concurrent.futures

HACKERNEWS_BASE_URL = os.environ.get('HACKERNEWS_BASE_URL', 'https://hacker-news.firebaseio.com/v0')
TOPSTORIES_URL = '{}/topstories.json'.format(HACKERNEWS_BASE_URL)
ITEM_URL = '{}/item/{item_id}.json'.format(HACKERNEWS_BASE_URL, item_id='{item_id}')

class APIClient(object):

    def get_top_stories_ids(self):
        response = requests.get(TOPSTORIES_URL)
        return response.json()

    def get_top_stories(self, max_number_of_stories = 500):
        top_stories_ids = self.get_top_stories_ids()
        n = min(max_number_of_stories, len(top_stories_ids))
        top_stories_ids = top_stories_ids[:n]
        stories_urls = [ITEM_URL.format(item_id=item_id) for item_id in top_stories_ids]
        return list(self.get_stories_concurrently(stories_urls))

    def get_stories_concurrently(self, stories_urls):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future_results = [executor.submit(requests.get, story) for story in stories_urls]
            concurrent.futures.wait(future_results)
            for future in future_results:
                yield future.result().json()

    def sort_stories_by_ranking(self, stories):
        return sorted(stories, key = lambda story : story['score'], reverse = True)
