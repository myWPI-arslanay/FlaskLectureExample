import os
import pytest
from app import app, db
from app.models import Room, Course, TeachingAssistant, TA_Assignment
from config import Config
import sqlalchemy as sqla


class TestConfig(Config):
    SQLALCHEMY_DATABASE_URI = 'sqlite://'
    SECRET_KEY = 'bad-bad-key'
    WTF_CSRF_ENABLED = False
    DEBUG = True
    TESTING = True



@pytest.fixture(scope='module')
def test_client():
    # create the flask application ; configure the app for tests
    flask_app = app
    app.config.from_object(TestConfig)

    # Flask provides a way to test your application by exposing the Werkzeug test Client
    # and handling the context locals for you.
    testing_client = flask_app.test_client()
 
    # Establish an application context before running the tests.
    ctx = flask_app.app_context()
    ctx.push()
 
    yield  testing_client 
    # this is where the testing happens!
 
    ctx.pop()

def init_rooms():
    allrooms = [{'building' : 'Fuller', 'roomNumber' : 'B46', 'capacity' : 60}, 
                    {'building' : 'UnityHall', 'roomNumber' : '175', 'capacity' : 100},
                    {'building' : 'UnityHall', 'roomNumber' : '150', 'capacity' : 80}]
    for room in allrooms:
        db.session.add(Room (building = room['building'],roomNumber=room['roomNumber'], capacity = room['capacity'] ))
    db.session.commit()   
    return None

@pytest.fixture
def init_database(request,test_client):
    # Create the database and the database table
    db.create_all()
    # initialize the topics
    init_rooms()
    yield  # this is where the testing happens!
    db.drop_all()

def test_createcourse(test_client,init_database):
    """ Tests creating new courses."""
    
    


 


