import app as main
from app import model, message
from flask.testing import FlaskClient
from flask import json
from os import path
TESTDB = "test.db"
TESTDB_PATH = path.abspath(path.dirname(__file__))
TEST_DATABASE_URI = "sqlite:///" + path.join(TESTDB_PATH, TESTDB)
