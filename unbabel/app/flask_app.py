from flask import Flask, render_template, jsonify
from os import environ
from database_wrapper import DatabaseWrapper

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template('index.html', translations=get_translations())

@app.route('/api/translations/status')
def translations_status():
    translations = get_translations()
    response = jsonify(translations)
    return response

def get_translations():
    fields_to_retrieve =  ['uid', 'status', 'text', 'source_language', 'target_language']
    return DatabaseWrapper().get_translations(fields_to_retrieve)

if __name__ == "__main__":
    app.run(host = '0.0.0.0', port = int(environ.get("PORT", 5000)))
