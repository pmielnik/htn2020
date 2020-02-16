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
       AND user_id = ?;
'''

SELECT_USER_BY_EMAIL = '''
    SELECT id FROM users
     WHERE email = ?;
'''

SELECT_ALL_USER_INFO = '''
    SELECT user.id, user.name, user.phone, user.picture, comp.name, loc.latitude,
           loc.longitude, GROUP_CONCAT(events.name)
      FROM users as user
      JOIN locations as loc
        ON user.location_id = loc.id
      JOIN companies as comp
        ON user.company_id = comp.id
      JOIN event_attendance as ea
        ON user.id = ea.user_id
      JOIN events
        ON events.id = ea.event_id
  GROUP BY user.id;
'''

SELECT_SINGLE_USER_INFO = '''
    SELECT user.id, user.name, user.phone, user.picture, comp.name, loc.latitude,
           loc.longitude, GROUP_CONCAT(events.name)
      FROM users as user
      JOIN locations as loc
        ON user.location_id = loc.id
      JOIN companies as comp
        ON user.company_id = comp.id
      JOIN event_attendance as ea
        ON user.id = ea.user_id
      JOIN events
        ON events.id = ea.event_id
     WHERE user.id = ?
  GROUP BY user.id;
'''

SELECT_ATTENDANCE_BY_USER = '''
    SELECT event_id FROM event_attendance
     WHERE user_id = ?;
'''

SELECT_ATTENDANCE_BY_EVENT = '''
    SELECT event_id FROM event_attendance
     WHERE event_id = ?;
'''

# Takes in a latiutde, longitude, and range
# order: lat, range, lat, range, long, range, long, range
SELECT_USERS_BY_LOCATION_RANGE = '''
    SELECT users.id, users.name
      FROM users
      JOIN locations as loc
        ON users.location_id = loc.id
     WHERE loc.lat >= (? - ?)
       AND loc.lat <= (? - ?)
       AND loc.long >= (? - ?)
       AND loc.long <= (? + ?);
'''

SELECT_EVENT_INFO_BY_ID = '''
    SELECT events.id, events.name, GROUP_CONCAT(users.id)
      FROM events
      JOIN event_attendance as ea
        ON events.id = ea.event_id
      JOIN users
        ON ea.user_id = users.id
     WHERE events.id = ?
  GROUP BY events.id;
'''