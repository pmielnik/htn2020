from flask import Flask, request, jsonify
import sqlite3
conn = sqlite3.connect('database/htn2020.db')

app = Flask(__name__)

#TODO: add to docs that you need to run "export FLASK_APP=main" and then run "flask run" to run the app

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/help')
def docs():
    return 'this is where docs will go lol'

@app.route('/users')
def users():
    #return a json payload of all users in the db
    return 'just me for now'

@app.route('/users/<user_id>')
def user_info(user_id):
    #reutrn json payload of single user
    return 'wow singled out huh?'

@app.route('/location', methods=['GET'])
def location_info():
    #return list of users who are located within range of loc
    lat = request.args.get('latitude')
    long = request.args.get('longitude')
    result_range = request.args.get('range')
    return 'no one here :('

@app.route('/events')
def events():
    #returns a list of event objects
    return 'nothin yet oops'

@app.route('/events/<event_id>')
def event_info(event_id):
    #return json obj with event info + attendees
    return 'wow such empty'

@app.route('/events/<event_id>/attendees', methods=['GET', 'POST'])
def event_attendeed(event_id):
    if request.method == 'GET':
        #simply return list of attendees
        return 'hah so many people'
    if request.method == 'POST':
        #register an attendee at the event, then return list of attendees
        return 'success!'