# -*- coding: utf-8 -*-

from flask import Flask, send_file, send_from_directory, jsonify, request
from marshmallow import Schema, fields

from friskis import FriskisClient

app = Flask(__name__)


class ShiftSchema(Schema):
    name = fields.String()
    venue = fields.String()
    leader_name = fields.String()
    start_dt = fields.DateTime()
    end_dt = fields.DateTime()
    available_places = fields.Integer()
    bookable_places = fields.Integer()
    total_places = fields.Integer()


@app.route('/activities')
def activities_list():
    client = FriskisClient()
    client.login(username='nip3o', password='J9yshwvCc7ccCGNjSw5c')
    shifts = client.get_available_shifts()

    schema = ShiftSchema(many=True)
    response = jsonify({
        'result': schema.dump(shifts).data,
    })
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