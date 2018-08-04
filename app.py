from flask import Flask, jsonify

app = Flask(__name__)


@app.route('/', methods=['GET'])
def get_home():
    return jsonify({
        'app_name': 'railways-api',
        'version': '0.1'
    })
