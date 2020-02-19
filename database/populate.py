import sqlite3
import json
from queries import *

conn = sqlite3.connect('htn2020.db')
c = conn.cursor()

with open('data.json') as json_file:
    data = json.load(json_file)
    #populate the db from the given data
    for obj in data:
        #check if company exists, if not, add it
        c.execute(SELECT_COMPANY_BY_NAME_SQL, [obj['company']])
        result = c.fetchone()
        if result == None:
            c.execute(ADD_COMPANY_SQL, [obj['company']])
            company_id = c.lastrowid
        else:
            company_id = result[0]

        #check if location exists, if not, add it
        c.execute(SELECT_LOCATION_BY_LS_SQL, [obj['latitude'], obj['longitude']])
        result = c.fetchone()
        if result == None:
            c.execute(ADD_LOCATION_SQL, [obj['latitude'], obj['longitude']])
            location_id = c.lastrowid
        else:
            location_id = result[0]
        
        events = []
        for event in obj['events']:
            event_id = None
            #check if event exists, if not, add it
            c.execute(SELECT_EVENT_BY_NAME_SQL, [event['name']])
            result = c.fetchone()
            if result == None:
                c.execute(CREATE_EVENT_SQL, [event['name']])
                event_id = c.lastrowid
            else:
                event_id = result[0]
            events.append(event_id)

        #create user if the email does not already exist
        c.execute(SELECT_USER_BY_EMAIL, [obj['email']]) 
        result = c.fetchone()
        if result == None:
            c.execute(CREATE_USER_SQL, (
                obj['name'],
                obj['email'],
                obj['phone'],
                obj['picture'],
                company_id,
                location_id
            ))
            user_id = c.lastrowid
        else:
            user_id = result[0]

        #mark user as attended for all events if they haven't been marked yet
        for event in events:
            if event:
                c.execute(SELECT_ATTENDANCE, [event, user_id])
                event_id = c.fetchone()
                if event_id == None:
                    c.execute(MARK_ATTENDANCE_SQL, [event, user_id])

        conn.commit()

conn.close()