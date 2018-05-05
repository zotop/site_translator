from flask import Flask, json, jsonify
from os import environ
from app.database_wrapper import DatabaseWrapper
from app.api_client import APIClient

app = Flask(__name__)

@app.route('/top_stories/<int:number_of_stories>')
def top_stories(number_of_stories):
    stories_with_comments = APIClient().get_top_stories_with_comments(number_of_stories)
    response = jsonify(stories_with_comments)
    response.status_code = 200
    return response

@app.route('/test_db_connection')
def test_db_connection():
    try:
        db = DatabaseWrapper()
        return json.dumps(db.client.server_info())
    except:
        return 'Failed to connect to mongo database'

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = int(environ.get("PORT", 5000)))
