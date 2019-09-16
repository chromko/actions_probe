from flask import Flask, request, make_response, Response, jsonify, abort, g
from threading import Thread
from functools import wraps

import sqlite3
import os
import json
import logging
import requests
import datetime
from models import db, User

# def get_db():
#     db = getattr(g, '_database', None)
#     if db is None:
#         db = g._database = sqlite3.connect(DATABASE)
#     return db


# def init_db():
    # User.create_all()


POSTGRES = {
    'user': 'postgres',
    'pw': 'password',
    'db': 'postgres',
    'host': 'localhost',
    'port': '5432',
}


logging.basicConfig(level=logging.INFO)
app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = ""
app.config['DATABASE_URI'] = 'postgresql://%(user)s:%(pw)s@%(host)s:%(port)s/%(db)s' % POSTGRES
db.init_app(app)
# init_db()


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


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
    return True


def count_birthday_delay(date):
    bday = datetime.datetime.strptime(date, '%Y-%m-%d')
    today = datetime.date.today()
    nextbday = 0
    if (bday.month, bday.day) < (today.month, today.day):
        nextbday = datetime.date(today.year + 1, bday.month, bday.day)
    else:
        nextbday = datetime.date(today.year, bday.month, bday.day)
    diff = (nextbday - today).days
    return diff


@app.route("/hello/<username>", methods=["PUT"])
@validate_username
def update_user_bd(username):
    if not request.json or 'dateOfBirth' not in request.json:
        abort(400)
    date = request.json['dateOfBirth']
    if validate_bd(date):
        try:
            rows = User.query.filter_by(username=username).update({'date': date})
            db.session.commit()
        except sqlite3.DatabaseError as err:
            print("Error: ", err)
            abort(500)
        return make_response("No Content", 204)
    return make_response("Fail", 500)


@app.route("/hello/<username>", methods=["GET"])
@validate_username
def get_user_bd(username):
    user = User.query.filter_by(username=username).first()
    if user is not None:
        delay = count_birthday_delay(user.date)
        if delay != 0:
            return make_response(jsonify(
                {'message': 'Hello {}! Your birthday is in {} days'.format(username, delay)}), 200)
        return make_response(jsonify(
            {'message': 'Hello {}! Happy Birthday!'.format(username)}), 200)
    else:
        abort(404)
        return None

if __name__ == "__main__":
    app.run(host="0.0.0.0")
