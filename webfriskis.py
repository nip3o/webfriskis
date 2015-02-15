# -*- coding: utf-8 -*-

import datetime

from flask import Flask, send_file, send_from_directory, jsonify

app = Flask(__name__)


@app.route('/activities')
def activities_list():
    response = jsonify({
        'result': [{
            'name': u'Gym öppet',
            'date': datetime.datetime.now().isoformat(),
            'placesLeft': 2,
            'placesTotal': 30,
            'time': '14:30 - 20:00',
            'location': 'Kanonhuset',
            'leader': '',
        }, {
            'name': u'Power Hour',
            'date': datetime.datetime.now().isoformat(),
            'placesLeft': 2,
            'placesTotal': 30,
            'time': '16:00 - 17:00',
            'location': 'Kanonhuset',
            'leader': 'Kaka Mupp',
        }]})
    response.status_code = 200
    return response


@app.route('/')
def index():
    return send_file('static/index.html')


@app.route('/static/<path:path>')
def staticfiles(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
