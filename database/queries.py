CREATE_EVENT_SQL = '''
    INSERT INTO events (name)
    VALUES (?);
'''

ADD_COMPANY_SQL = '''
    INSERT INTO companies (name)
    VALUES (?);
'''

ADD_LOCATION_SQL = '''
    INSERT INTO locations (latitude, longitude)
    VALUES (?, ?);
'''

CREATE_USER_SQL = '''
    INSERT INTO users (name, email, phone, picture, company_id, location_id)
    VALUES (?, ?, ?, ?, ?, ?);

'''

MARK_ATTENDANCE_SQL = '''
    INSERT INTO event_attendance (event_id, user_id)
    VALUES (?, ?);
'''

SELECT_EVENT_BY_NAME_SQL = '''
    SELECT id FROM events
     WHERE name = ?;
'''

SELECT_COMPANY_BY_NAME_SQL = '''
    SELECT id FROM companies
     WHERE name = ?;
'''

SELECT_LOCATION_BY_LS_SQL = '''
    SELECT id FROM locations
     WHERE latitude = ?
       AND longitude = ?;
'''

SELECT_ATTENDANCE = '''
    SELECT event_id FROM event_attendance
     WHERE event_id = ?
       AND user_id = ?
'''

SELECT_USER_BY_EMAIL = '''
    SELECT id FROM users
     WHERE email = ?
'''