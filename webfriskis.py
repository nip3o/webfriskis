# -*- coding: utf-8 -*-
import os

from werkzeug.contrib.cache import MemcachedCache
from flask import Flask, send_file, send_from_directory, jsonify, request

from marshmallow import Schema, fields

from friskis import FriskisClient

app = Flask(__name__)
cache = MemcachedCache(['127.0.0.1:11211'])

SHIFTS_CACHE_KEY = 'activities'
CACHE_TIMEOUT = 5 * 60


class ShiftSchema(Schema):
    uid = fields.String()
    name = fields.String()
    venue = fields.String()
    leader_name = fields.String()
    start_dt = fields.DateTime()
    end_dt = fields.DateTime()
    booked_places = fields.Integer()
    bookable_places = fields.Integer()
    total_places = fields.Integer()


@app.route('/activities')
def activities_list():
    schema = ShiftSchema(many=True)
    shifts = cache.get(SHIFTS_CACHE_KEY)

    if not shifts:
        client = FriskisClient()
        client.login(username=os.environ['FRISKIS_USERNAME'],
                     password=os.environ['FRISKIS_PASSWORD'])

        shifts = list(client.get_available_shifts())
        cache.set(SHIFTS_CACHE_KEY, shifts, timeout=CACHE_TIMEOUT)

    response = jsonify({
        'result': schema.dump(shifts).data,
    })
    response.status_code = 200
    return response


@app.route('/activities/<uid>/book', methods=['POST'])
def book(uid):
    schema = ShiftSchema()

    client = FriskisClient()
    client.login(username=os.environ['FRISKIS_USERNAME'],
                 password=os.environ['FRISKIS_PASSWORD'])

    for shift in client.get_available_shifts():
        if shift.uid == uid:
            shift.book(client.session)

    shift.booked_places += 1
    shift.bookable_places -= 1

    response = jsonify(schema.dump(shift).data)
    response.status_code = 200
    return response


@app.route('/login', methods=['POST'])
def login():
    client = FriskisClient()
    client.login(username=request.form['username'],
                 password=request.form['password'])

    return client.session


@app.route('/')
def index():
    return send_file('static/index.html')


@app.route('/static/<path:path>')
def staticfiles(path):
    return send_from_directory('static', path)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
