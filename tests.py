import unittest
from unittest.mock import patch, Mock, MagicMock, call
from app import app
from flask import Flask, request, make_response, Response, jsonify, abort, g
import datetime


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
        self.badRequestStatus = "400 BAD REQUEST"
        self.notFountStatus = "404 Not Found"
        self.noContentOKStatus = "204 No Content"

    def test_validate_username_invalids(self):
        with app.test_client() as client:
            for testCase, testValue in self.invalidUsernames.items():
                resp = client.get('/hello/' + testValue)
                print(testCase + ":" + testValue)
                self.assertEqual(resp.status, self.badRequestStatus)

    def test_validate_username_valids(self):
        with app.test_client() as client:
            for testCase, testValue in self.validUsernames.items():
                resp = client.get('/hello/' + testValue)
                print(testCase + ":" + testValue)
                self.assertEqual(resp.status, self.noContentOKStatus)

    def test_get_user_bd(self):


    def count_birthday_delay(self):


    def validate_date():


if __name__ == '__main__':
    unittest.main()
