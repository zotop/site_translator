from flask import Flask, render_template, jsonify
from os import environ
from database_wrapper import DatabaseWrapper

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('index.html')

@app.route('/api/translations/status')
def translations_status():
    fields_to_retrieve =  ['uid', 'status', 'text', 'source_language', 'target_language']
    translations = DatabaseWrapper().get_translations(fields_to_retrieve)
    print(translations)
    response = jsonify(translations)
    #response.status_code = 200
    return response

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = int(environ.get("PORT", 5000)))
