from flask import Flask, request, make_response, Response, jsonify,abort
from threading import Thread
from functools import wraps

import sqlite3
import os
import json
import logging
import requests
import datetime

from requests.auth import HTTPBasicAuth
from operator import itemgetter
from urllib.parse import urlencode

from slackclient import SlackClient

logging.basicConfig(level=logging.INFO)

app = Flask(__name__)
conn = sqlite3.connect("users.db")
cursor = conn.cursor()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


def validate_username(func):
    @wraps(func)
    def validator(*args, **kwargs):
        username = kwargs['username']
        if not username.isalpha():
            logging.error("Error: username is invalid!")
            abort(400)
        return func(*args, **kwargs)
    return validator


def validate_bd(date):
    try:
        datetime.datetime.strptime(date, '%Y-%m-%d')
    except ValueError:
        raise ValueError("Incorrect data format, should be YYYY-MM-DD")
    if datetime.datetime.strptime(date, '%Y-%m-%d') == datetime.date.today():
        return False


@app.route("/hello/<username>", methods=["PUT"])
@validate_username
def update_user_bd(username):
    if not request.json or 'dateOfBirth' not in request.json:
        abort(400)
    date = request.json['dateOfBirth']
    if validate_bd(date):
        print('TRUE')
        try:
            cursor.execute("INSERT INTO bdays VALUES (?, ?)", username, date)
            result = cursor.fetchall()
            print(result)
        except sqlite3.DatabaseError as err:
            print("Error: ", err)
            abort(500)
        else:
            conn.commit()
        return make_response("No Content", 204)
    return make_response("Fail", 500)


@app.route("/hello/<username>", methods=["GET"])
@validate_username
def get_user_bd(username):
    try:
        cursor.execute("SELECT date FROM bdays where username = '?' ", username)
        result = cursor.fetchall()
        print(result)
        return make_response(jsonify(
            {'message': 'Hello {}! Your birthday is in {} days'.format(username, result)
            }),200)
    except sqlite3.DatabaseError as err:
        print("Error: ", err)


if __name__ == "__main__":
    app.run(host="0.0.0.0")
