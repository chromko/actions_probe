from flask import Flask, request, make_response, Response, jsonify, abort, g,
from flask_sqlalchemy import SQLAlchemy
from threading import Thread
from functools import wraps

import sqlite3
import os
import json
import logging
import requests
import datetime
# from config import Config


def create_app():
    app = Flask(__name__)
    return app


def get_db(db):
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


def init_db(db, file='schema.sql'):
    with app.app_context():
        db = get_db(DATABASE)
        with app.open_resource(file, mode='r') as f:
            db.cursor().executescript(f.read())
        db.commit()

DATABASE = "users.db"
logging.basicConfig(level=logging.INFO)

# app.config.from_object(Config)
db = SQLAlchemy(app)
# db = get_db(DATABASE)


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


@app.errorhandler(400)
def bad_requestq    (error):
    return make_response(jsonify({'error': 'Bad request'}), 400)


def validate_username(func):
    @wraps(func)
    def validator(*args, **kwargs):
        username = kwargs['username']
        if not username.isalpha():
            logging.error("Error: username is invalid!")
            abort(400)
            return None
        try:
            username.encode('ascii')
        except UnicodeEncodeError:
            abort(400)
            return None
        return func(*args, **kwargs)
    return validator


def validate_date(date):
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
    db = get_db(DATABASE)
    cursor = db.cursor()
    # cursor = db.cursor()
    if not request.json or 'dateOfBirth' not in request.json:
        abort(400)
        return None
    date = request.json['dateOfBirth']
    if validate_date(date):
        try:
            cursor.execute('''INSERT INTO BDAYS(USERNAME,DATE) VALUES(?, ?)
            ON CONFLICT(USERNAME)
            DO UPDATE SET DATE=excluded.date''',
            (username, date))
            db.commit()
        except sqlite3.DatabaseError as err:
            print("Error: ", err)
            abort(500)
        return make_response("No Content", 204)
    return make_response("Fail", 500)


@app.route("/hello/<username>", methods=["GET"])
@validate_username
def get_user_bd(username):
    db = get_db(DATABASE)
    cursor = db.cursor()
    try:
        birthdate = cursor.execute("SELECT DATE FROM BDAYS where USERNAME=?", (username,)).fetchone()[0]
        delay = count_birthday_delay(birthdate)
        if delay != 0:
            return make_response(jsonify(
                {'message': 'Hello {}! Your birthday is in {} days'.format(username, delay)}), 200)
        return make_response(jsonify(
            {'message': 'Hello {}! Happy Birthday!'.format(username)}), 200)
    except sqlite3.DatabaseError as err:
        print("Error: ", err)
    else:
        make_response("Fail", 500)


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0")
