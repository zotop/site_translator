from flask import Flask, json
from os import environ
from database_wrapper import DatabaseWrapper

app = Flask(__name__)

@app.route('/test_db_connection')
def test_db_connection():
    try:
        db = DatabaseWrapper()
        return json.dumps(db.client.server_info())
    except:
        return 'Failed to connect to mongo database'

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = int(environ.get("PORT", 5000)))
