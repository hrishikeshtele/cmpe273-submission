import uuid
from datetime import datetime

import validators
from flask import Flask, jsonify, request, redirect
from marshmallow import ValidationError

import encode
from model import *

app = Flask(__name__)

"""
Generating unique numbers for each link by encoding counter which starts from a specific value.
This guarantees a unique value for each link hence collision case is altogether averted.
"""


def get_counter(data):
    if 'counter' not in data:
        data["counter"] = 1000000000
    data["counter"] += 1
    return data["counter"]


@app.route('/shorten', methods=['POST'], endpoint='shorten')
def shorten():
    content = request.json
    req_model = ShortenReq()
    try:
        result = req_model.load(content)
        error = validate_url(result["long_url"])
        if error is not None:
            return error
        error = validate_url(result["domain"])
        if error is not None:
            return {"error": "domain not valid eg. http://localhost:5000"}, 400
        bitlink_id = encode.base62_encode(get_counter(session))
        if result["domain"][-1] == '/':
            link = result["domain"][:-1] + "/" + bitlink_id
        else:
            link = result["domain"] + "/" + bitlink_id
        value = UrlData(link, str(uuid.uuid4()), result["long_url"],
                        datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), "", [], 0)
        session[link] = value
        response = ShortenRes(value.link, value.id, value.long_url, value.created_at)
    except ValidationError as err:
        return jsonify(err.messages), 400

    return response.to_json(), 200


@app.route('/create', methods=['POST'], endpoint='create')
def create():
    content = request.json
    req_model = CreateReq()
    try:
        result = req_model.load(content)
        error = validate_url(result["long_url"])
        if error is not None:
            return error
        bitlink_id = encode.base62_encode(get_counter(session))
        link = result["domain"] + "/" + bitlink_id
        value = UrlData(link, str(uuid.uuid4()), result["long_url"],
                        datetime.now().strftime("%m/%d/%Y, %H:%M:%S"), result['title'],
                        result["tags"], 0)
        session[link] = value
        response = CreateRes(value.link, value.id, value.long_url, value.created_at, value.title, value.tags)
    except ValidationError as err:
        return jsonify(err.messages), 400

    return response.to_json(), 200


@app.route('/bitlinks/<path:bitlink>', methods=['PATCH'], endpoint='update_link')
def update_link(bitlink: str):
    error = validate_url(bitlink)
    if error is not None:
        return error
    content = request.json
    req_model = UpdateReq()
    try:
        result = req_model.load(content)
        if bitlink is not None and bitlink in session:
            v: UrlData = session[bitlink]
            if result['long_url'] is not None and not "":
                error = validate_url(result['long_url'])
                if error is not None:
                    return error
                v.long_url = result['long_url']
            if result['title'] is not None:
                v.title = result['title']
            if result['tags'] is not None:
                v.tags = result['tags']
            response = UpdateRes(v.link, v.id, v.long_url, v.created_at, v.title, v.tags)
        else:
            return {"error": "bitlink not found"}, 404
    except ValidationError as err:
        return jsonify(err.messages), 400

    return response.to_json(), 200


@app.route('/bitlinks/<path:bitlink>', methods=['GET'], endpoint='get')
def get(bitlink: str):
    error = validate_url(bitlink)
    if error is not None:
        return error
    if bitlink is not None and bitlink in session:
        v: UrlData = session[bitlink]
        if v is not None:
            return UpdateRes(v.link, v.id, v.long_url, v.created_at, v.title, v.tags).to_json(), 200
    return {"error": "bitlink not found"}, 404


@app.route('/bitlinks/<path:bitlink>/clicks', methods=['GET'], endpoint='get_clicks')
def get_clicks(bitlink: str):
    error = validate_url(bitlink)
    if error is not None:
        return error
    if bitlink is not None and bitlink in session:
        v: UrlData = session[bitlink]
        return ClickRes(v.link, str(v.hits), v.long_url, v.created_at).to_json(), 200
    else:
        return {"error": "bitlink not found"}, 404


@app.route('/<path:bitlink>', methods=['GET'], endpoint='hit_link')
def hit_link(bitlink: str):
    error = validate_url(request.url)
    if error is not None:
        return error
    link = request.url
    if link is not None and session.get(link):
        v: UrlData = session[link]
        v.hits += 1
        return redirect(v.long_url, code=302)
    else:
        return {"error": "bitlink not found"}, 404


def validate_url(url):
    valid = validators.url(url)
    if not valid:
        return {"error": "long_url/bitlink not valid"}, 400


session = {}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
