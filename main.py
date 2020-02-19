from flask import Flask, request, jsonify
import sqlite3
from database.queries import *

conn = sqlite3.connect('database/htn2020.db',check_same_thread=False)
conn.row_factory = sqlite3.Row  # to receve dictionaries from db queries
c = conn.cursor()

app = Flask(__name__)

#TODO: add to docs that you need to run "export FLASK_APP=main" and then run "flask run" to run the app

#TODO: fix GROUP_BY fields to at least be an array and not simply a list of strs

#TODO: fix db lol

# formats the result, which is a list fo sqlite3.Row objects, into a
# JSON object with the specified cols as keys
def json_format(result, cols, type_name=None):
    data = []
    for row in result:
        if row != None && type_name != None:
            data.append({type_name : dict(zip(cols, row))})
        if row != None && type_name == None:
            data.append(dict(zip(cols, row)))
    
    return jsonify(data)

@app.route('/')
def hello_world():
    return 'Hello, World!'

@app.route('/help')
def docs():
    return 'this is where docs will go lol'

@app.route('/users')
def users():
    #return a json payload of all users in the db
    c.execute(SELECT_ALL_USER_INFO)
    result = c.fetchall()

    return json_format(result, SELECT_ALL_USER_INFO_COLS, 'user')

@app.route('/users/<user_id>')
def user_info(user_id):
    #reutrn json payload of single user
    c.execute(SELECT_SINGLE_USER_INFO, user_id)
    result = c.fetchone()

    return json_format([result], SELECT_SINGLE_USER_INFO_COLS, 'user')

@app.route('/location', methods=['GET'])
def location_info():
    #return list of users who are located within range of loc
    lat = float(request.args.get('latitude'))
    long = float(request.args.get('longitude'))
    result_range = float(request.args.get('range'))

    print(long)
    print(lat)

    c.execute(SELECT_USERS_BY_LOCATION_RANGE, [lat-result_range, lat+result_range, 
                                               long-result_range, long+result_range])
    result = c.fetchall()

    return json_format(result, SELECT_USERS_BY_LOCATION_RANGE_COLS)

@app.route('/events')
def events():
    #returns a list of event objects
    c.execute(SELECT_ALL_EVENT_INFO)
    result = c.fetchall()

    return json_format(result, SELECT_ALL_EVENT_INFO_COLS, 'event')

@app.route('/events/<event_id>')
def event_info(event_id):
    #return json obj with event info + attendees
    c.execute(SELECT_EVENT_INFO_BY_ID, event_id)
    result = c.fetchone()
    #TODO: add full attendee user objects instead of just IDs

    return json_format([result], SELECT_EVENT_INFO_BY_ID_COLS)

@app.route('/events/<event_id>/attendees', methods=['GET', 'POST'])
def event_attendeed(event_id):
    if request.method == 'GET':
        #simply return list of attendees
        c.execute(SELECT_ATTENDANCE_BY_EVENT, event_id)
        result = c.fetchone()

        return json_format([result], SELECT_ATTENDANCE_BY_EVENT_COLS, 'attendee')
    if request.method == 'POST':
        #register an attendee at the event, then return list of attendees
        # TODO: make sure user_id actually exists first (or throw appropriate error code)
        user_id = request.args.get('user_id')
        c.execute(MARK_ATTENDANCE_SQL, [event_id, user_id])
        conn.commit()
        
        #if not crashed:
        return format('success: registered user {0} for event {1}', user_id, event_id)