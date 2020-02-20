from flask import Flask, request, jsonify, Response
import sqlite3
from database.queries import *

conn = sqlite3.connect('database/htn2020.db',check_same_thread=False)
conn.row_factory = sqlite3.Row  # to receve dictionaries from db queries
c = conn.cursor()

app = Flask(__name__)

#################################### Helper Functions ####################################

# formats the result, which is a list fo sqlite3.Row objects, into a
# JSON object with the specified cols as keys
def json_format(result, cols, type_name=None, group_concat=None):
    data = []
    for row in result:
        if row != None and type_name != None and group_concat != None:
            # change field from list of strings to array of ids
            # each instance of cols in queries.py is defined as having the list od strs as the last element
            single_data = dict(zip(cols, row))
            list_obj = single_data[group_concat].split(',')
            if(group_concat == 'user_ids'):
                single_data[group_concat] = [int(v) for v in list_obj]
            else:
                single_data[group_concat] = list_obj
            data.append({type_name : single_data})
        elif row != None and type_name != None:
            data.append({type_name : dict(zip(cols, row))})
        elif row != None and type_name == None:
            data.append(dict(zip(cols, row)))
    
    return jsonify(data)

def json_format_single(result, cols, type_name=None, group_concat=None):
    for row in result:
        if row != None and type_name != None and group_concat != None:
            # change field from list of strings to array of ids
            # each instance of cols in queries.py is defined as having the list od strs as the last element
            single_data = dict(zip(cols, row))
            list_obj = single_data[group_concat].split(',')
            if(group_concat == 'user_ids'):
                single_data[group_concat] = [int(v) for v in list_obj]
            else:
                single_data[group_concat] = list_obj
            return jsonify({type_name : single_data})
        elif row != None and type_name != None:
            return jsonify({type_name : dict(zip(cols, row))})
        elif row != None and type_name == None:
            return jsonify(dict(zip(cols, row)))

#################################### API Definitions ####################################
@app.route('/')
def hello_world():
    return 'Hack the North 2020 Backend Dev Challenge Server'

@app.route('/help')
def docs():
    return ('''
        The following endpoints are currently supported by this API:\n
        - /users: GET\n
        - /users/<user_id>: GET\n
        - /location: GET\n
        - /events: GET\n
        - /events/<event_id>: GET\n
        - /events/<event_id>/attendees: GET/POST\n
        \n
        For more information, please see https://github.com/pmielnik/htn2020
    ''')

@app.route('/users')
def users():
    #return a json payload of all users in the db
    c.execute(SELECT_ALL_USER_INFO)
    result = c.fetchall()

    return json_format(result, SELECT_ALL_USER_INFO_COLS, 'user', 'attended_events')

@app.route('/users/<user_id>')
def user_info(user_id):
    #ensure user_id exists
    c.execute(SELECT_USER_BY_ID_CHECK, [user_id])
    result = c.fetchone()
    if result == None:
        return Response('ERROR: no user with id {0}'.format(user_id), status=403)

    #reutrn json payload of single user
    c.execute(SELECT_SINGLE_USER_INFO, [user_id])
    result = c.fetchone()

    return json_format_single([result], SELECT_SINGLE_USER_INFO_COLS, 'user', 'attended_events')

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

    return json_format(result, SELECT_ALL_EVENT_INFO_COLS, 'event', 'user_ids')

@app.route('/events/<event_id>')
def event_info(event_id):
    #return json obj with event info + attendees
    c.execute(SELECT_EVENT_INFO_BY_ID, [event_id])
    result = c.fetchone()
    #add full attendee user objects to replace user ids returned in query
    if result != None:
        data = dict(zip(SELECT_EVENT_INFO_BY_ID_COLS, result))
        data['attendees'] = []
        users = data['user_ids'].split(',')
        for user_id in users:
            c.execute(SELECT_SINGLE_USER_INFO, [user_id])
            result = c.fetchone()
            data['attendees'].append(dict(zip(SELECT_SINGLE_USER_INFO_COLS, result)))
        
        #remove unnecessary field
        del data['user_ids']
        return jsonify(data)
    
    return Response('ERROR: event {0} does not exist'.format(event_id), status=403)

@app.route('/events/<event_id>/attendees', methods=['GET', 'POST'])
def event_attendeed(event_id):
    #ensure event_id exists
    c.execute(SELECT_EVENT_BY_ID_CHECK, [event_id])
    result = c.fetchone()
    if result == None:
        return Response('ERROR: no event with id {0}'.format(event_id), status=403)
    if request.method == 'GET':
        #simply return list of attendees
        c.execute(SELECT_ATTENDANCE_BY_EVENT, [event_id])
        result = c.fetchall()

        return json_format(result, SELECT_ATTENDANCE_BY_EVENT_COLS, 'attendee')
    elif request.method == 'POST':
        #register an attendee at the event, then return list of attendees
        user_id = request.args.get('user_id')

        #ensure user id exists
        c.execute(SELECT_USER_BY_ID_CHECK, [user_id])
        result = c.fetchone()
        if result == None:
            return Response('ERROR: no user with id {0}'.format(user_id), status=403)

        c.execute(MARK_ATTENDANCE_SQL, [event_id, user_id])
        conn.commit()
        
        #if not crashed:
        return Response('SUCCESS: registered user {0} for event {1}'.format(user_id, event_id), status=200)