import unittest
from unittest.mock import patch, Mock, MagicMock, call
from app import app, db
from flask import Flask, request, make_response, Response, jsonify, abort, g
import datetime
import os


class BaseTest(unittest.TestCase):
    def setUp(self):
        # self.mock_connection = Mock()
        self.validUsernames = {"user1": "user"}
        self.invalidUsernames = {
            "number": "test1",
            "specSymbol1": "test^",
            "specSymbol2": "test:",
            "notLatin": "testЫ"
        }
        basedir = os.path.abspath(os.path.dirname(__file__))
        db_name = 'test.db'
        self.db_uri = 'sqlite:///' + os.path.join(basedir, db_name)
        app.config['TESTING'] = True
        app.config['WTF_CSRF_ENABLED'] = False
        app.config['SQLALCHEMY_DATABASE_URI'] = self.db_uri
        db.create_all()

        self.badRequestStatus = "400 BAD REQUEST"
        self.notFountStatus = "404 Not Found"
        self.noContentOKStatus = "204 No Content"

        # self.users_bd = ""
        # self.app = app.test_client()
        # self.db = get_db(db_name)
        # init_db(self.db, file="seed.sql")

    def test_validate_username_invalids(self):
        for testCase, testValue in self.invalidUsernames.items():
            resp = self.app.get('/hello/' + testValue)
            print(testCase + ":" + testValue)
            self.assertEqual(resp.status, self.badRequestStatus)

    # def test_validate_username_valids(self):
    #     for testCase, testValue in self.validUsernames.items():
    #         resp = self.app.get('/hello/' + testValue)
    #         print(testCase + ":" + testValue)
    #         self.assertEqual(resp.status, self.noContentOKStatus)

    # def test_get_user_bd(self):
    #     with app.test_client() as client:


    # def count_birthday_delay(self):


    # def validate_date():


if __name__ == '__main__':
    unittest.main()
